import pyb
from board import sys_config
#from hts221 import HTS221
from ism43362 import ISM43362

if 1 == 0:
    i2c = pyb.I2C(sys_config['hts221']['i2c_bus'],
                  pyb.I2C.MASTER, baudrate=100000)
    hts221 = HTS221(i2c, sys_config['hts221']['i2c_addr'])
    hts221.print_calib()
    print("Humidity    = %4.1f %%" % hts221.humidity())
    print("Temperature =  %2.1f C" % hts221.temperature())
if 1==0:
    mag = LIS3MDL(i2c, sys_config['lis3mdl']['i2c_addr'])
    x, y, z = mag.xyz()
    print("Magnetic field = (%.3e, %.3e, %.3e) %s" % (x, y, z, mag.unit()))

    #p = LPS25H(i2c, sys_config['lps25h']['i2c_addr'])
    print("Pressure %5.3e %s, Height %.1f m, Temperature = %.1f C" %
          (p.value(), p.unit(), p.height(), p.temperature()))

    #dist = VL6180X(i2c, sys_config['vl6180x']['i2c_addr'])
    val = dist.dev_id()
    print("Distance sensor:")
    print("\n".join(["  %s: %s" % (k, v) for k, v in val.items()]))
    print("Distance      %.1f %s" % (dist.value(), dist.unit()))

wifi_com=pyb.SPI(sys_config['ism43362']['spi_bus'],pyb.SPI.MASTER,
                 baudrate=1000000,
                 bits=sys_config['ism43362']['spi_bits'],
                 polarity=sys_config['ism43362']['CPOL'],
                 phase=sys_config['ism43362']['CPHA'])
wifi_sel=pyb.Pin(sys_config['ism43362']['spi_cs'], pyb.Pin.OUT_PP)
wifi_ready=pyb.Pin(sys_config['ism43362']['ready'], pyb.Pin.IN)
wifi_reset=pyb.Pin(sys_config['ism43362']['reset'], pyb.Pin.OUT_PP)
wifi_wakeup=pyb.Pin(sys_config['ism43362']['wakeup'], pyb.Pin.OUT_PP)
wifi = ISM43362(wifi_com, wifi_sel, wifi_reset, wifi_ready, wifi_wakeup)
