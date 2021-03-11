from enum import Enum, auto
import struct
import math


class DataTypes(Enum):
    U8 = auto()
    S8 = auto()
    U16 = auto()
    S16 = auto()
    U32 = auto()
    S32 = auto()
    U64 = auto()
    S64 = auto()
    U128 = auto()
    F32 = auto()
    STR = auto()

    @classmethod
    def listItems(cls):
        lst = [
                DataTypes.U8,
                DataTypes.S8,
                DataTypes.U16,
                DataTypes.S16,
                DataTypes.U32,
                DataTypes.S32,
                DataTypes.U64,
                DataTypes.S64,
                DataTypes.U128,
                DataTypes.F32,
                DataTypes.STR
                ]
        return lst

    @classmethod
    def fromStr(cls, s):
        """ Return a value from the string, return None if
            no string matches...
            MAYBE the programmer got the wrong type in
            their argument s.  So we accept it directly if it's
            already a good DataType
        """
        if s in cls.listItems():
            # oops - but forgiven
            return s

        if s == 'U8':
            return DataTypes.U8
        elif s == 'S8':
            return DataTypes.S8
        elif s == 'U16':
            return DataTypes.U16
        elif s == 'S16':
            return DataTypes.S16
        elif s == 'U32':
            return DataTypes.U32
        elif s == 'U16':
            return DataTypes.U16
        elif s == 'S32':
            return DataTypes.S32
        elif s == 'U64':
            return DataTypes.U64
        elif s == 'S64':
            return DataTypes.S64
        elif s == 'U128':
            return DataTypes.U128
        elif s == 'F32':
            return DataTypes.F32
        elif s == 'STR':
            return DataTypes.STR
        return None

    def __str__(self):
        if DataTypes.U8 == self:
            return "U8"
        if DataTypes.S8 == self:
            return "S8"
        elif DataTypes.U16 == self:
            return "U16"
        elif DataTypes.S16 == self:
            return "S16"
        elif DataTypes.U32 == self:
            return "U32"
        elif DataTypes.S32 == self:
            return "S32"
        elif DataTypes.U64 == self:
            return "U64"
        elif DataTypes.S64 == self:
            return "S64"
        elif DataTypes.U128 == self:
            return "U128"
        elif DataTypes.F32 == self:
            return "F32"
        elif DataTypes.STR == self:
            return "STR"
        return "?unknown"

    def LenBytes(self):
        if DataTypes.U8 == self:
            return 1
        if DataTypes.S8 == self:
            return 1
        elif DataTypes.U16 == self:
            return 2
        elif DataTypes.S16 == self:
            return 2
        elif DataTypes.U32 == self:
            return 4
        elif DataTypes.S32 == self:
            return 4
        elif DataTypes.U64 == self:
            return 8
        elif DataTypes.S64 == self:
            return 8
        elif DataTypes.U128 == self:
            return 16
        elif DataTypes.F32 == self:
            return 4
        elif DataTypes.STR == self: 
            return 0
        return 0

    def IsSigned(self):
        if DataTypes.S8 == self:
            return True
        elif DataTypes.S16 == self:
            return True
        elif DataTypes.S32 == self:
            return True
        elif DataTypes.S64 == self:
            return True
        elif DataTypes.F32 == self:
            return True
        return False
    
    def IsAtomic(self):
        if DataTypes.U8 == self:
            return True
        elif DataTypes.S8 == self:
            return True
        elif DataTypes.U16 == self:
            return True
        return False

    def CountOfModbusWords(self):
        return int((self.LenBytes() + 1)/2)

    def ReverseWordsInBytearray(self, byte_array):
        l = len(byte_array)
        reversed_arr = bytearray(l)
        for i in range(0,l,2):
            reversed_arr[i:i+2] = byte_array[l-i-2:l-i]
        return reversed_arr

    def BytearrayToData(self, byte_array):
        """ Converts a bytearray from a modbus telegram into data of its own type """
        if (self.CountOfModbusWords()*2 != len(byte_array)):            
            return None                     #TODO raise error
        data = None        
        if DataTypes.U8 == self:
            if byte_array[0] != 0:
                return None                 #TODO raise error
            else:
                data = (byte_array[0] << 8) + byte_array[1]
        elif DataTypes.S8 == self:
            if byte_array[0] != 0:
                return None                 #TODO raise error
            else:
                data = int.from_bytes( byte_array[1].to_bytes(1,'big') , "big", signed=True)
        elif DataTypes.U16 == self:
            data = int.from_bytes( byte_array , "big", signed=False)
        elif DataTypes.S16 == self:
            data = int.from_bytes( byte_array , "big", signed=True)
        elif (DataTypes.U32 == self) or (DataTypes.U64 == self) or (DataTypes.U128 == self):
            reversed_arr = self.ReverseWordsInBytearray(byte_array)
            data = int.from_bytes( reversed_arr , "big", signed=False)
        elif (DataTypes.S32 == self) or (DataTypes.S64 == self):
            reversed_arr = self.ReverseWordsInBytearray(byte_array)
            data = int.from_bytes( reversed_arr , "big", signed=True)   
        elif DataTypes.F32 == self:
            reversed_arr = self.ReverseWordsInBytearray(byte_array)
            data = struct.unpack('>f', reversed_arr)[0] 
        elif DataTypes.STR == self:
            pass 
        return data                         #TODO raise error
    
    def DataToBytearray(self, data):
        """ Converts data into a bytearray to be transmitted on a modbus telegram"""
        l_bytes = self.CountOfModbusWords()*2
        byte_array = bytearray(l_bytes)
        if DataTypes.U8 == self:
            byte_array[1] = data
        elif DataTypes.S8 == self:
            byte_array[1] = data.to_bytes(1,'big', signed=True)[0]
        elif DataTypes.U16 == self:
            byte_array = data.to_bytes(l_bytes,'big', signed=False)        
        elif DataTypes.S16 == self:
            byte_array = data.to_bytes(l_bytes,'big', signed=True)
        elif (DataTypes.U32 == self) or (DataTypes.U64 == self) or (DataTypes.U128 == self):
            byte_array = data.to_bytes(l_bytes,'big', signed=False)
            byte_array = self.ReverseWordsInBytearray(byte_array)
        elif (DataTypes.S32 == self) or (DataTypes.S64 == self):
            byte_array = data.to_bytes(l_bytes,'big', signed=True)
            byte_array = self.ReverseWordsInBytearray(byte_array)
        elif DataTypes.F32 == self:
            byte_array = struct.pack('>f', data)
            byte_array = self.ReverseWordsInBytearray(byte_array)
        return byte_array


if "__main__" == __name__:
    print("Command line self demo:")
    for x in DataTypes:
        print(str(x) + " length implied is " + str(x.LenBytes()))
        print(" Signed " + str(x.IsSigned()))
        print(" Atomic " + str(x.IsAtomic()))
        print(" CountOfModbusWords " + str(x.CountOfModbusWords()))

        d = DataTypes.fromStr(x)
        if d == x:
            print(
                  " DataTypes.fromStr test noddy error: "
                  + " == "
                  + str(d)
                  + " no problem."
                  )
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("Failed stupid noddy error type change not needed")
            print("Failed on " + str(x))
            sys.exit(1)

        y = str(x)
        d = DataTypes.fromStr(y)
        if d == x:
            print(
                  " DataTypes.fromStr test: "
                  + y
                  + " == "
                  + str(d)
                  + " no problem."
                  )
        else:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("  DataTypes.fromStr(...) failed for " + str(d))
            sys.exit(1)

        if not x in DataTypes.listItems():
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("  DataTypes.listItems(...) doesn't include " + str(d))
            sys.exit(1)

    print()
    print("DataTypes.fromStr negative test, should fail == None.")
    x = DataTypes.fromStr('STR17')
    if x == None:
        print("yup, OK.")
    else:
        print("nope, " + str(x))
    print()
    print("Did you want to see a list of all the DataType enums.")
    print("Use DataTypes.listItems()")
    for x in DataTypes.listItems():
        print("  " + str(x))
    print()
    print("All done.")

    # some tests
    print('\nBytearrayToData tests:')
    def test_BytearrayToData(byte_array, expected_value, data_type):
        value = data_type.BytearrayToData(byte_array)
        if isinstance(expected_value, float):
            are_equal = math.isclose(value, expected_value, rel_tol=1e-6)
        else:
            are_equal = (value == expected_value)
        if not are_equal:
            print(f'{data_type}.BytearrayToData() | FAIL | {value} != {expected_value}' )
        else:
            print(f'{data_type}.BytearrayToData() | OK')
    test_BytearrayToData( bytearray([0x00,0x80]), 128, DataTypes.U8)
    test_BytearrayToData( bytearray([0x00,0x80]), -128, DataTypes.S8)
    test_BytearrayToData( bytearray([0xFC,0x18]), 64536, DataTypes.U16)
    test_BytearrayToData( bytearray([0xFC,0x18]), -1000, DataTypes.S16)
    test_BytearrayToData( bytearray([0xCC,0xBC,0xEE,0xDD]), 4007513276, DataTypes.U32)
    test_BytearrayToData( bytearray([0xCC,0xBC,0xEE,0xDD]), -287454020, DataTypes.S32)
    test_BytearrayToData( bytearray([0x88,0x77,0xAA,0x99,0xCC,0xBB,0xEE,0xDD]), 17212138457273043063, DataTypes.U64)
    test_BytearrayToData( bytearray([0x88,0x77,0xAA,0x99,0xCC,0xBB,0xEE,0xDD]), -1234605616436508553, DataTypes.S64)
    test_BytearrayToData( bytearray([0x11,0x00,0x33,0x22,0x55,0x44,0x77,0x66,0x99,0x88,0xBB,0xAA,0xDD,0xCC,0xFF,0xEE]), 340193404210632335760508365704335069440, DataTypes.U128)
    test_BytearrayToData( bytearray([0xD6,0x80,0xBD,0xFC]), -0.123456, DataTypes.F32)

    print('\nDataToBytearray tests:')
    def test_DataToBytearray(data, expected_bytearray, data_type):
        byte_array = data_type.DataToBytearray(data)
        are_equal = (byte_array == expected_bytearray)
        if not are_equal:
            print(f'{data_type}.DataToBytearray() | FAIL | {byte_array} != {expected_bytearray}' )
        else:
            print(f'{data_type}.DataToBytearray() | OK')
    test_DataToBytearray(128, bytearray([0x00,0x80]), DataTypes.U8)
    test_DataToBytearray(-128, bytearray([0x00,0x80]), DataTypes.S8)
    test_DataToBytearray(64536, bytearray([0xFC,0x18]), DataTypes.U16)
    test_DataToBytearray(-1000, bytearray([0xFC,0x18]), DataTypes.S16)
    test_DataToBytearray(4007513276, bytearray([0xCC,0xBC,0xEE,0xDD]), DataTypes.U32)
    test_DataToBytearray(-287454020, bytearray([0xCC,0xBC,0xEE,0xDD]), DataTypes.S32)
    test_DataToBytearray(17212138457273043063, bytearray([0x88,0x77,0xAA,0x99,0xCC,0xBB,0xEE,0xDD]), DataTypes.U64)
    test_DataToBytearray(-1234605616436508553, bytearray([0x88,0x77,0xAA,0x99,0xCC,0xBB,0xEE,0xDD]), DataTypes.S64)
    test_DataToBytearray(340193404210632335760508365704335069440, bytearray([0x11,0x00,0x33,0x22,0x55,0x44,0x77,0x66,0x99,0x88,0xBB,0xAA,0xDD,0xCC,0xFF,0xEE]), DataTypes.U128)
    test_DataToBytearray(-0.123456, bytearray([0xD6,0x80,0xBD,0xFC]), DataTypes.F32)

    