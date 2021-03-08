import logging

from modbus_lib.modbus_serial import ModbusSerialLayer
from modbus_lib.modbus_application import ModbusApplicationLayer
import modbus_lib.exceptions as execps


class ModbusMaster():
    def __init__(self, ser, response_timeout_s, interframe_timeout_s, is_logger_on=True, logger_level=logging.DEBUG):
        """[summary]

        Args:
            ser (serial port): The serial port used
            response_timeout_s (float): Time in seconds to wait for a transmission. None is used to wait forever (slave)
            interframe_timeout_s (float): Time in seconds to decide end of frame
            is_logger_on (bool, optional): [description]. Defaults to True.
            logger_level ([type], optional): [description]. Defaults to logging.DEBUG.
        """
        self.logger = logging.getLogger('modbus_lib')
        self.logger.setLevel(logger_level)
        self.is_logger_on = is_logger_on
        self.serial_layer = ModbusSerialLayer(ser, response_timeout_s, interframe_timeout_s, is_logger_on)
        self.app_layer = ModbusApplicationLayer(is_logger_on)

    def read_holding_registers(self, slave_address, starting_address, quantity_registers):
        if (quantity_registers < 1) or (quantity_registers > 125):
            if self.is_logger_on:
                self.logger.debug(f'Number of registers requested out of range: {quantity_registers}')
                self.logger.error('RequestNumberRegistersError')
            raise execps.RequestNumberRegistersError
        pdu = self.app_layer.f3_create_request_pdu(starting_address, quantity_registers)
        response_pdu = self.serial_layer.send_request_unicast(slave_address, pdu)
        data = self.app_layer.f3_data_from_response_pdu(response_pdu, quantity_registers*2)
        return data
    
    def write_multiple_registers(self, slave_address, starting_address, quantity_registers, registers_value):
        if (quantity_registers < 1) or (quantity_registers > 123):
            if self.is_logger_on:
                self.logger.debug(f'Number of registers to write out of range: {quantity_registers}')
                self.logger.error('WriteNumberRegistersError')
            raise execps.WriteNumberRegistersError
        if len(registers_value) != (quantity_registers*2):
            if self.is_logger_on:
                self.logger.debug(f'Number of registers size different than register_value size: {quantity_registers*2}/{len(registers_value)}')
                self.logger.error('WriteDataLengthError')
            raise execps.WriteDataLengthError   
        pdu = self.app_layer.f16_create_request_pdu(starting_address, quantity_registers, registers_value)
        response_pdu = self.serial_layer.send_request_unicast(slave_address, pdu)
        self.app_layer.f16_validate_response_pdu(response_pdu, starting_address, quantity_registers)