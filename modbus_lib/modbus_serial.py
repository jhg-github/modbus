import time
import struct

import modbus_lib.exceptions as execps
from modbus_lib.utils import calc_crc


INTERFRAME_TIMEOUT_S = 0.01
RESPONSE_TIMEOUT_S = 1



# ---- crc --------------------------------------------------------------------
def is_crc_ok(frame):
    if len(frame) >=3:
        crc_calc = calc_crc(frame[:-2])
        crc_reply = struct.unpack('>H',frame[-2:])[0]
        if crc_calc == crc_reply:   
            return True
    return False


# ---- receive ----------------------------------------------------------------

def receive_only_interframe_timeout(ser, response_timeout_s, interframe_timeout_s):
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
    ser.timeout = response_timeout_s
    rx_byte = ser.read(1)
    if rx_byte == bytearray():
        raise execps.ResponseTimeoutError()
    rx_byte_start = time.time()
    rx_frame += rx_byte
    # read rest of bytes
    ser.timeout = 0
    while (time.time() - rx_byte_start) <= interframe_timeout_s:
        rx_byte = ser.read(1)
        if rx_byte:
            rx_byte_start = time.time()
            rx_frame += rx_byte
    return rx_frame

def receive_for_slave(ser):
    return receive_only_interframe_timeout(ser, None, INTERFRAME_TIMEOUT_S)



# ---- send -------------------------------------------------------------------

def send_request_unicast(ser, slave_addr, pdu):
    '''Sends a request to a single slave and waits for reply
    Serial Line PDU (Address, Function Code, Data, CRC)

    :param serial_port ser: The serial port sending/receiving the request/reply
    :param int slave_addr: The slave modbus addres [1-247]
    :param byte_array pdu: Modbus Protocol Data Unit (Function Code, Data)
    :return: slave reply pdu
    :rtype: byte_array
    :raises ReplyFrameNOKError: If reply frame contains a CRC error
    :raises ResponseTimeoutError: If a reply from slave is not receive on time
    '''
    # create serial line pdu
    serial_line_pdu = bytearray([1,3,0,126,0,2,164,19])
    #
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    # send serial line pdu
    print('TX:', serial_line_pdu.hex())
    ser.write(serial_line_pdu)
    # wait reply
    try:
        retry = True    # forces at least one iteration
        rest_of_response_time = RESPONSE_TIMEOUT_S
        start = time.time()
        # check correct slave replied 
        while retry:        
            reply = receive_only_interframe_timeout(ser, rest_of_response_time, INTERFRAME_TIMEOUT_S) # In case of a reply received from an unexpected slave, the Response time-out is kept running
            elapsed = time.time() - start
            rest_of_response_time = RESPONSE_TIMEOUT_S - elapsed
            if (reply[0] != slave_addr) and (rest_of_response_time > 0):
                retry= True
            else:
                retry= False            
        # check CRC
        if is_crc_ok(reply):
            return reply
        raise execps.ReplyFrameNOKError
    except execps.ResponseTimeoutError:
        raise execps.ResponseTimeoutError


def send_request_broadcast():
    pass

