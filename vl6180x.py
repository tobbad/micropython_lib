#
#
#
from i2cspi import COM_I2C
from multibyte import multibyte
from vl6180x_const import *
import pyb

class VL6180X(COM_I2C, multibyte):

    WHO_IAM_ANSWER = 0xB4
    WHO_IAM_REG = 0x00

    DEFAULT_CONF = VL6180X_DEFAULT_CONF

    def __init__(self, communication, dev_selector):
        super(VL6180X, self).__init__(communication, dev_selector, self.ADDR_MODE_16, self.TRANSFER_MSB_FIRST)
        data = self.read(VL6180X_SYSTEM_FRESH_OUT_OF_RESET)
        if data != 1:
            print("System already initialized")
        else:
            self.init()

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

    def value(self):
        self.write(VL6180X_SYSRANGE_START, 0x01) # Start Single shot mode
        pyb.delay(10)
        return self.read(VL6180X_RESULT_RANGE_VAL)

    def unit(self):
        return "mm"

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

