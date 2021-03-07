import time
import struct
import logging

import modbus_lib.exceptions as execps
from modbus_lib.utils import calc_crc


INTERFRAME_TIMEOUT_S = 0.01
RESPONSE_TIMEOUT_S = 1


class ModbusSerialLayer():
    def __init__(self, ser, response_timeout_s, interframe_timeout_s, is_logger_on=True):
        '''
        :param serial port ser: The serial port
        :param float response_timeout_s: Time in seconds to wait for a transmission. None is used to wait forever (slave)
        :param float interframe_timeout_s: Time in seconds to decide end of frame
        :return: The receive frame
        '''    
        self.ser = ser
        self.response_timeout_s = response_timeout_s
        self.interframe_timeout_s = interframe_timeout_s
        self.logger = logging.getLogger('modbus_lib')
        self.is_logger_on = is_logger_on


# ---- receive ----------------------------------------------------------------

    def receive_only_interframe_timeout(self, response_timeout_s, interframe_timeout_s):
        '''
        :param float response_timeout_s: Time in seconds to wait for a transmission. None is used to wait forever (slave)
        :param float interframe_timeout_s: Time in seconds to decide end of frame
        :return: The receive frame
        :rtype: bytearray
        :raises ResponseTimeoutError: If no transmission is received before response_timeout_s
        '''
        # init
        rx_frame = bytearray()
        # wait first byte
        self.ser.timeout = response_timeout_s
        rx_byte = self.ser.read(1)
        if rx_byte == bytearray():
            if self.is_logger_on:
                self.logger.error('ResponseTimeoutError')
            raise execps.ResponseTimeoutError()
        rx_byte_start = time.time()
        rx_frame += rx_byte
        # read rest of bytes
        self.ser.timeout = 0
        while (time.time() - rx_byte_start) <= interframe_timeout_s:
            rx_byte = self.ser.read(1)  #TODO read all in buffer? for reception without fails
            if rx_byte:
                rx_byte_start = time.time()
                rx_frame += rx_byte
        if self.is_logger_on:
            self.logger.debug(f'RX: {rx_frame.hex()}')
        return rx_frame

    def receive_for_slave(self):
        return self.receive_only_interframe_timeout(None, self.interframe_timeout_s)



# # ---- send -------------------------------------------------------------------

    def send_frame(self, frame):
        self.ser.write(frame)
        if self.is_logger_on:
            self.logger.debug(f'TX: {frame.hex()}')

    def send_request_unicast(self, slave_addr, pdu):
        '''Sends a request to a single slave and waits for reply
        Serial Line PDU (Address, Function Code, Data, CRC)

        :param int slave_addr: The slave modbus addres [1-247]
        :param byte_array pdu: Modbus Protocol Data Unit (Function Code, Data)
        :return: slave reply pdu
        :rtype: byte_array
        :raises ReplyFrameNOKError: If reply frame contains a CRC error
        :raises ResponseTimeoutError: If a reply from slave is not receive on time
        '''
        # create serial line pdu
        if slave_addr < 1 or slave_addr > 247:
            self.logger.error(f'RequestSlaveIdError. Slave Id out of range: {slave_addr}')
            raise execps.RequestSlaveIdError
        serial_line_pdu = self.create_serial_pdu(slave_addr, pdu )
        #
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        # send serial line pdu
        self.send_frame(serial_line_pdu)
        # wait reply
        try:
            retry = True    # forces at least one iteration
            rest_of_response_time = RESPONSE_TIMEOUT_S
            start = time.time()
            # check correct slave replied 
            while retry:        
                reply = self.receive_only_interframe_timeout(rest_of_response_time, self.interframe_timeout_s) # In case of a reply received from an unexpected slave, the Response time-out is kept running
                elapsed = time.time() - start
                rest_of_response_time = RESPONSE_TIMEOUT_S - elapsed
                if (reply[0] != slave_addr) and (rest_of_response_time > 0):
                    retry= True
                else:
                    retry= False            
            # check CRC
            if self.is_crc_ok(reply):
                return self.pdu_from_frame(reply)
            if self.is_logger_on:
                self.logger.error('ReplyFrameNOKError')
            raise execps.ReplyFrameNOKError
        except execps.ResponseTimeoutError:
            raise execps.ResponseTimeoutError


# def send_request_broadcast():
#     pass


# ---- utils --------------------------------------------------------------------
    @staticmethod
    def is_crc_ok(frame):
        if len(frame) >=3:
            crc_calc = calc_crc(frame[:-2])
            crc_reply = struct.unpack('>H',frame[-2:])[0]
            if crc_calc == crc_reply:   
                return True
        return False
    
    @staticmethod
    def create_serial_pdu(slave_address, pdu):
        #TODO raise invalid slave address
        serial_pdu = bytearray([slave_address])
        serial_pdu += pdu
        crc_calc = calc_crc(serial_pdu)
        serial_pdu += crc_calc.to_bytes(2, byteorder='big')
        return serial_pdu
    
    @staticmethod
    def pdu_from_frame(frame):
        return frame[1:-2]