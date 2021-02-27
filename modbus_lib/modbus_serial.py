import time


INTERFRAME_TIMEOUT_S = 0.00175
RESPONSE_TIMEOUT = 0.5


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

def receive_for_server(ser):
    return receive_only_interframe_timeout(ser, None, INTERFRAME_TIMEOUT_S)

def receive_for_client(ser):
    return receive_only_interframe_timeout(ser, RESPONSE_TIMEOUT, INTERFRAME_TIMEOUT_S)