
import pyb
from board import config
from conf import conf
from time import sleep


rp = pyb.Pin('PE3', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
rp.high()

i2c = pyb.I2C(1, pyb.I2C.MASTER, baudrate=100000)

spi = pyb.SPI(2, pyb.SPI.MASTER, baudrate=600000, polarity=1, phase=1)


if conf==0:
    from l3gd20 import L3GD20
    from lsm303c import LSM303C
    from mfx import MFX
    cs_gyro = pyb.Pin('PD7', pyb.Pin.OUT_PP)
    gyro = L3GD20(spi, cs_gyro)
    # gyro.DEBUG = False
    print("Gyro = (%7.2f %7.2f, %7.2f)" % gyro.xyz())
    print("Temperature = %.1f C" % gyro.temperature())
    cs_accel = pyb.Pin('PE0', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
    cs_mag = pyb.Pin('PC0', pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
    mems = LSM303C(spi, cs_mag, cs_accel)
    mems.bidi_mode()
    mems.exists()
    print("Accel = (%6.4f, %6.4f, %6.4f)" % mems.accel.xyz())
    print("Mag   = (%6.4f, %6.4f, %6.4f)" % (mems.mag.xyz()))
elif conf==1:
    i2c_mfx = pyb.I2C(config['mfx']['i2c_bus'], pyb.I2C.MASTER, baudrate=100000)
    wake_up_mfx = pyb.Pin(config['mfx']['wakeUp_pin'], pyb.Pin.OUT_PP, pyb.Pin.PULL_NONE)
    irq_mfx = pyb.Pin(config['mfx']['irq_pin'], pyb.Pin.IN, pyb.Pin.PULL_DOWN)
    conf = IDD_DEFAULT()
    mfx = MFX(i2c_mfx, config['mfx']['i2c_addr'], wake_up_mfx, conf, irq_mfx)
elif conf==2:
    #
    # Test reaction time on UART transfers
    #
    from uart_idle import UART_IDLE 
    uart = pyb.UART(2, baudrate = 115200, timeout=1)
    dut=UART_IDLE(uart)
    dut.set_up_cb()
    callback= uart.irq()
    callback()    # call the callback
    print("Trigger flag %d " % uart.irq().trigger()) # Print active set triggers
    # Enable IRQ
    uart.irq().enable()
elif conf == 3:
    from mgc3x30 import MGC3X30, SW_ADDR
    reset_pin = pyb.Pin('PA2', pyb.Pin.OUT_PP)
    transfer_pin = pyb.Pin('PA1', pyb.Pin.PULL_UP)
    mgc = MGC3X30(reset_pin, transfer_pin, i2c, SW_ADDR )
    while True:
        print(mgc.read_binary(0, 26))
        sleep(1)    
       
