import pyb
from board import sys_config
from hts221 import HTS221

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
