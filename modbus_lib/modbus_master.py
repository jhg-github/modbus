import logging

from modbus_lib.modbus_serial import ModbusSerialLayer
import modbus_lib.modbus_application as ModApp


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
        self.serial_layer = ModbusSerialLayer(ser, response_timeout_s, interframe_timeout_s, is_logger_on)

    def read_holding_register(self, slave_address, starting_address, quantity_registers):
        pdu = ModApp.f3_create_request_pdu(starting_address, quantity_registers)
        response_pdu = self.serial_layer.send_request_unicast(slave_address, pdu)
        data = ModApp.data_from_response_pdu(response_pdu, 3, quantity_registers*2)
        return data
