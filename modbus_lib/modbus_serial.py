import time


INTERFRAME_TIMEOUT_S = 0.005
RESPONSE_TIMEOUT = 0.5


# ---- receive ----------------------------------------------------------------

def receive_only_interframe_timeout(ser, first_byte_timeout, interframe_timeout):
    # init
    rx_buffer = bytearray()
    # wait first byte
    ser.timeout = first_byte_timeout
    rx_byte = ser.read(1)
    rx_start = time.time()
    rx_buffer += rx_byte
    # read rest of bytes
    ser.timeout = 0
    while (time.time() - rx_start) <= interframe_timeout:
        rx_byte = ser.read(1)
        if rx_byte:
            rx_start = time.time()
            rx_buffer += rx_byte
    return rx_buffer

def receive_for_slave(ser):
    return receive_only_interframe_timeout(ser, None, INTERFRAME_TIMEOUT_S)

def receive_for_master(ser):
    return receive_only_interframe_timeout(ser, RESPONSE_TIMEOUT, INTERFRAME_TIMEOUT_S)


# ---- send -------------------------------------------------------------------

def send_request_unicast(ser, slave_addr, pdu):
    '''Sends a request to a single slave and waits for reply
    Serial Line PDU (Address, Function Code, Data, CRC)

    :param serial_port ser: The serial port sending/receiving the request/reply
    :param int slave_addr: The slave modbus addres [1-247]
    :param byte_array pdu: Modbus Protocol Data Unit (Function Code, Data)
    :return: XXX
    :rtype: XXX
    :raises XXXError: if XXX
    :raises XXXError: if XXX
    '''
    # create serial line pdu
    # send serial line pdu
    # wait reply
    # check correct slave replied 
            # In case of a reply received from an unexpected slave, the Response time-out is kept running
            # In case of an error detected on the frame, a retry may be performed
    pass

def send_request_broadcast():
    pass

