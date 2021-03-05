import struct

import modbus_lib.exceptions as exceps

# class Response():
#     def __init__(self, requested_function, response_pdu):
#         self.function = response_pdu[0]
#         self.data = None
#         self.exception_code = None
#         if self.function == requested_function:
#             self.data = response_pdu[1:]
#         elif self.function == ( requested_function & 0x80):
#             self.exception_code = response_pdu[1]
#             raise exceps.MosbusException
#         else:
#             raise exceps.ModbusUnknownException
            
        

def f3_create_request_pdu(starting_address, quantity_registers):
    pdu = bytearray([3])
    pdu += struct.pack('>H',starting_address)
    pdu += struct.pack('>H',quantity_registers)
    return pdu

def data_from_response_pdu(response_pdu, requested_function, requested_bytes):
    function = response_pdu[0]
    if function == requested_function:
        data = response_pdu[1:]
        if len(data) == requested_bytes:
            return data
        else:
            raise exceps.ModbusInvalidResponseLengthError
    elif function == ( requested_function & 0x80):
        exception_code = response_pdu[1]
        if exception_code == 1:
            raise exceps.ModbusExceptionIllegalFunction
        elif exception_code == 2:
            raise exceps.ModbusExceptionIllegalDataAddress
        elif exception_code == 3:
            raise exceps.ModbusExceptionIllegalDataValue
        elif exception_code == 4:
            raise exceps.ModbusExceptionServerDeviceFailure
        elif exception_code == 5:
            raise exceps.ModbusExceptionAcknowledge
        elif exception_code == 6:
            raise exceps.ModbusExceptionServerDeviceBusy        
    raise exceps.ModbusUnknownException


if __name__ == "__main__":
    print(f3_create_request_pdu(107,3).hex())