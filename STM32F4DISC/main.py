

from staccel import STAccel
acc = STAccel()


def run():
    while True:
        print("%5.2g %5.2f %5.2f" % (acc.x(), acc.y(), acc.z()))
        pyb.delay(100)


from  CS43L22 import CS43L22
snd = CS43L22()
