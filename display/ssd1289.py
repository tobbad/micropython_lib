

class SSD1289_com:

    # Copy modify paste from LBF_OLED_Init default configuration which is
    # taken from DD-160128FC-1A.pdf
 
    def __init__(self, bus, rs, wr, cs, rst):
        self._bus = bus
        self._rs = rs
        self._wr = wr
        self._cs = cs
        self._rst = rst
        self._bus.init(self._bus.WRITE)
        self._rs.init(self._rs.OUT_PP)
        self._wr.init(self._wr.OUT_PP)
        self._cs.init(self._cs.OUT_PP)
        self._rst.init(self._rst.OUT_PP)
        
    def write_bus(self, data):
        ''' lowest level write to databus'''
        self._bus.write(data)
        self._wr.value(0)
        self._wr.value(1)
        
        
    def write_com(self, data):
        ''' Write configuration data'''
        self._rs.value(0)
        self.write_bus(data&0x00FF)
    
    def write_data(self, data):
        ''' Write data'''
        self._rs.value(1)
        self.write_bus(data)
        
    def write_com_data(self, com_data, data):
        ''' Write data'''
        self.write_com(com_data)
        self.write_data(data)
    
    def select(self, state):
        ''' Set the cs to a certain state'''
        self._cs.value(state<0)
        
    def reset(self):
        '''Reset display '''
        pass
        
        
