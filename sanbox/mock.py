from sanbox.data_types import DataTypes

class MockClass():
    def __init__(self):
        # self.registers = { 130 : { 'd_type' : DataTypes.F32, 'value' : -0.123456 } }
        self.registers = { 130 : { 'd_type' : DataTypes.F32, 'value' : 987.236 } }
    
    def get_reg_data(self, addr):
        reg = self.registers[addr]
        return reg['d_type'].DataToBytearray( reg['value'] )