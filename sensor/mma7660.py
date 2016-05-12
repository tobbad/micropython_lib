"""
"""
from i2cspi import COM_I2C
from multibyte import multibyte

MMA7660_X_ADDR = const(0x00)  # Output Register X
MMA7660_Y_ADDR = const(0x01)  # Output Register Y
MMA7660_Z_ADDR = const(0x02)  # Output Register Z


class MMA7660(COM_I2C, multibyte):
    #
    # Debug
    #
    DEFAULT_CONF = [
        (0x07, 0x01),]

    WHO_IAM_ANSWER = 0
    WHO_IAM_REG = 0
    WHO_IAM_ANSWER_MASK = 0x00

    def __init__(self, communication, dev_selector):
        """
        Create a MMA7660 device.
        """
        super().__init__(communication, dev_selector,
                         self.ADDR_MODE_8,
                         self.TRANSFER_MSB_FIRST)
        self.init()

    def _reg2val(self, reg):
        val =self.read_u8(reg)
        val &= 0x3F
        val = val-64 if val >=32 else val
        return val


    def x(self):
        """
        Get angular velocity around x axis in degree per second.
        """
        return self._reg2val(MMA7660_X_ADDR)

    def y(self):
        """
        Get angular velocity around y axis.in degree per second.
        """
        return self._reg2val(MMA7660_Y_ADDR)

    def z(self):
        """
        Get angular velocity around z axis in degree per second.
        """
        return self._reg2val(MMA7660_Z_ADDR)

    def xyz(self):
        """
        Get tuple of all angular velocities in degree per second.
        """
        return (self.x(), self.y(), self.z())
