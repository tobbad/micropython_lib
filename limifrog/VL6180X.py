#
#
#
import sensor_i2c
import pyb
from VL6180X_const import *

class VL6180X(sensor_i2c.sensor_i2c):

    WHOAMI_ANS = 0xB4
    WHO_IAM_REG = 0x00
    debug = False

    def __init__(self, bus=2, addr = 0x29):
        super(VL6180X, self).__init__(bus, addr, self.ADDR_MODE_16)
        data = self.read(VL6180X_SYSTEM_FRESH_OUT_OF_RESET)
        if data != 1:
            print("System already initialized")
        self.write(0x0207, 0x01)
        self.write(0x0208, 0x01)
        self.write(0x0096, 0x00)
        self.write(0x0097, 0xfd)
        self.write(0x00e3, 0x00)
        self.write(0x00e4, 0x04)
        self.write(0x00e5, 0x02)
        self.write(0x00e6, 0x01)
        self.write(0x00e7, 0x03)
        self.write(0x00f5, 0x02)
        self.write(0x00d9, 0x05)
        self.write(0x00db, 0xce)
        self.write(0x00dc, 0x03)
        self.write(0x00dd, 0xf8)
        self.write(0x009f, 0x00)
        self.write(0x00a3, 0x3c)
        self.write(0x00b7, 0x00)
        self.write(0x00bb, 0x3c)
        self.write(0x00b2, 0x09)
        self.write(0x00ca, 0x09)
        self.write(0x0198, 0x01)
        self.write(0x01b0, 0x17)
        self.write(0x01ad, 0x00)
        self.write(0x00ff, 0x05)
        self.write(0x0100, 0x05)
        self.write(0x0199, 0x05)
        self.write(0x01a6, 0x1b)
        self.write(0x01ac, 0x3e)
        self.write(0x01a7, 0x1f)
        self.write(0x0030, 0x00)
        # Recommended settings from datasheet
        # http:# www.st.com/st-web-ui/static/active/en/resource/technical/document/application_note/DM00122600.pdf
        # Enable Interrupts on Conversion Complete (any source)
        self.write(VL6180X_SYSTEM_INTERRUPT_CONFIG_GPIO, (4 << 3)|(4) ) #  Set GPIO1 high when sample complete
        self.write(VL6180X_SYSTEM_MODE_GPIO1, 0x10) #  Set GPIO1 high when sample complete
        self.write(VL6180X_READOUT_AVERAGING_SAMPLE_PERIOD, 0x30) # Set Avg sample period
        self.write(VL6180X_SYSALS_ANALOGUE_GAIN, 0x46) #  Set the ALS gain
        self.write(VL6180X_SYSRANGE_VHV_REPEAT_RATE, 0xFF) #  Set auto calibration period (Max = 255)/(OFF = 0)
        self.write(VL6180X_SYSALS_INTEGRATION_PERIOD, 0x63) #  Set ALS integration time to 100ms
        self.write(VL6180X_SYSRANGE_VHV_RECALIBRATE, 0x01) #  perform a single temperature calibration
        # Optional settings from datasheet
        # http:# www.st.com/st-web-ui/static/active/en/resource/technical/document/application_note/DM00122600.pdf
        self.write(VL6180X_SYSRANGE_INTERMEASUREMENT_PERIOD, 0x09) #  Set default ranging inter-measurement period to 100ms
        self.write(VL6180X_SYSALS_INTERMEASUREMENT_PERIOD, 0x0A) #  Set default ALS inter-measurement period to 100ms
        self.write(VL6180X_SYSTEM_INTERRUPT_CONFIG_GPIO, 0x24) #  Configures interrupt on ‘New Sample Ready threshold event’
        # Additional settings defaults from community
        self.write(VL6180X_SYSRANGE_MAX_CONVERGENCE_TIME, 0x32)
        self.write(VL6180X_SYSRANGE_RANGE_CHECK_ENABLES, 0x10 | 0x01)
        self.write_u16(VL6180X_SYSRANGE_EARLY_CONVERGENCE_ESTIMATE, 0x7B )
        self.write_u16(VL6180X_SYSALS_INTEGRATION_PERIOD, 0x64)

        self.write(VL6180X_READOUT_AVERAGING_SAMPLE_PERIOD,0x30)
        self.write(VL6180X_SYSALS_ANALOGUE_GAIN,0x40)
        self.write(VL6180X_FIRMWARE_RESULT_SCALER,0x01)

    def dev_id(self):
        res = {}
        res['idModel'] =  self.read(VL6180X_IDENTIFICATION_MODEL_ID)
        res['idModelRevMajor'] = self.read(VL6180X_IDENTIFICATION_MODEL_REV_MAJOR)
        res['idModelRevMinor'] = self.read(VL6180X_IDENTIFICATION_MODEL_REV_MINOR)
        res['idModuleRevMajor'] = self.read(VL6180X_IDENTIFICATION_MODULE_REV_MAJOR)
        res['idModuleRevMinor'] = self.read(VL6180X_IDENTIFICATION_MODULE_REV_MINOR)
        res['idDate'] = self.read_u16(VL6180X_IDENTIFICATION_DATE)
        res['idTime'] = self.read_u16(VL6180X_IDENTIFICATION_TIME)
        return res

    def distance(self):
        self.write(VL6180X_SYSRANGE_START, 0x01) # Start Single shot mode
        pyb.delay(10)
        return self.read(VL6180X_RESULT_RANGE_VAL)

    def ambient_light(self, gain):
        if not gain in VL6180X_GAIN:
            raise Exception("Unsupported gain %s" % gain)
        regGain =  VL6180X_GAIN[gain]
        # First load in Gain we are using, do it everytime incase someone changes it on us.
        # Note: Upper nibble shoudl be set to 0x4 i.e. for ALS gain of 1.0 write 0x46
        self.write(VL6180X_SYSALS_ANALOGUE_GAIN, (0x40 | regGain)) #  Set the ALS gain
        # Start ALS Measurement
        self.write(VL6180X_SYSALS_START, 0x01)

        pyb.delay(100) # give it time...

        self.write(VL6180X_SYSTEM_INTERRUPT_CLEAR, 0x07)

        # Retrieve the Raw ALS value from the sensoe
        alsRaw = self.read_u16(VL6180X_RESULT_ALS_VAL)

        # Get Integration Period for calculation, we do this everytime incase someone changes it on us.
        alsIntegrationPeriodRaw = self.read_u16(VL6180X_SYSALS_INTEGRATION_PERIOD)

        alsIntegrationPeriod = 100.0 / alsIntegrationPeriodRaw

        # Calculate actual LUX from Appnotes

        alsGain = 0.0

        if (gain== "20"):
            alsGain = 20.0
        elif (gain == "10"):
            alsGain = 10.32
        elif (gain == "5.0"):
            alsGain = 5.21
        elif (gain == "2.5"):
            alsGain = 2.60
        elif (gain == "1.67"):
            alsGain = 1.72
        elif (gain == "1.25"):
            alsGain = 1.28
        elif (gain == "1.0"):
            alsGain = 1.01
        elif (gain == "40"):
            alsGain = 40.0
        else:
            print("Unknown Gain %s" % gain)

        # Calculate LUX from formula in AppNotes
        alsCalculated = 0.32 * (float(alsRaw) / alsGain) * alsIntegrationPeriod

        return alsCalculated

