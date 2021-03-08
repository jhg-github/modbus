import struct
import logging

import modbus_lib.exceptions as exceps

    
class ModbusApplicationLayer():
    def __init__(self, is_logger_on=True):
        self.logger = logging.getLogger('modbus_lib')
        self.is_logger_on = is_logger_on
    
    def raise_modbus_exception(self, response_pdu):
        exception_code = response_pdu[1]
        if exception_code == 1:
            if self.is_logger_on:
                self.logger.error('ModbusExceptionIllegalFunction')
            raise exceps.ModbusExceptionIllegalFunction
        elif exception_code == 2:
            if self.is_logger_on:
                self.logger.error('ModbusExceptionIllegalDataAddress')
            raise exceps.ModbusExceptionIllegalDataAddress
        elif exception_code == 3:
            if self.is_logger_on:
                self.logger.error('ModbusExceptionIllegalDataValue')
            raise exceps.ModbusExceptionIllegalDataValue
        elif exception_code == 4:
            if self.is_logger_on:
                self.logger.error('ModbusExceptionServerDeviceFailure')
            raise exceps.ModbusExceptionServerDeviceFailure
        elif exception_code == 5:
            if self.is_logger_on:
                self.logger.error('ModbusExceptionAcknowledge')
            raise exceps.ModbusExceptionAcknowledge
        elif exception_code == 6:
            if self.is_logger_on:
                self.logger.error('ModbusExceptionServerDeviceBusy')
            raise exceps.ModbusExceptionServerDeviceBusy    

    def f3_create_request_pdu(self, starting_address, quantity_registers):
        pdu = bytearray([3])
        pdu += struct.pack('>H',starting_address)
        pdu += struct.pack('>H',quantity_registers)
        return pdu
        
    def f3_data_from_response_pdu(self, response_pdu, requested_bytes):
        requested_function = 3
        function = response_pdu[0]
        if function == requested_function:
            byte_count = response_pdu[1]
            data = response_pdu[2:]
            if (byte_count == requested_bytes) and (len(data) == requested_bytes):
                return data
            else:
                if self.is_logger_on:
                    self.logger.debug(f'Requested bytes: {requested_bytes} - Received bytes: {len(data)}')
                    self.logger.error('ModbusInvalidResponseLengthError')
                raise exceps.ModbusInvalidResponseLengthError
        elif function == ( requested_function | 0x80):
            self.raise_modbus_exception(response_pdu)   
        if self.is_logger_on:
            self.logger.error('ModbusUnknownException')    
        raise exceps.ModbusUnknownException

    def f16_create_request_pdu(self, starting_address, quantity_registers, registers_value):
        pdu = bytearray([16])
        pdu += struct.pack('>H',starting_address)
        pdu += struct.pack('>H',quantity_registers)
        pdu += struct.pack('B',quantity_registers*2)
        pdu += registers_value
        return pdu

    def f16_validate_response_pdu(self, response_pdu, expected_starting_addres, expected_quantity_registers):
        requested_function = 16
        function = response_pdu[0]
        if function == requested_function:
            starting_address = struct.unpack('>H',response_pdu[2:3])[0]
            quantity_registers = struct.unpack('>H',response_pdu[3:5])[0]
            if (starting_address == expected_starting_addres) and (quantity_registers == expected_quantity_registers):
                return
            else:
                if self.is_logger_on:
                    self.logger.debug(f'Start address: {starting_address}/{expected_starting_addres} - Quantity: {quantity_registers}/{expected_quantity_registers}')
                    self.logger.error('InvalidWriteResponseError')
                raise exceps.InvalidWriteResponseError
        elif function == ( requested_function | 0x80):
            self.raise_modbus_exception(response_pdu)   
        if self.is_logger_on:
            self.logger.error('ModbusUnknownException')    
        raise exceps.ModbusUnknownException


if __name__ == "__main__":
    app_layer = ModbusApplicationLayer(True)
    print(app_layer.f3_create_request_pdu(107,3).hex())
    print(app_layer.f16_create_request_pdu(21, 3, bytearray([1,2,3,4,5,6])).hex())