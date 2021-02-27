import serial
import time


def receive_simplified_with_timeout(ser, timeout):
    # init
    rx_buffer = bytearray()
    # wait first byte
    ser.timeout = None
    rx_byte = ser.read(1)
    rx_start = time.time()
    rx_buffer += rx_byte
    # read rest of bytes
    ser.timeout = 0
    while (time.time() - rx_start) <= timeout:
        rx_byte = ser.read(1)
        if rx_byte:
            rx_start = time.time()
            rx_buffer += rx_byte
    return rx_buffer


ser = serial.Serial('/dev/ttyACM0', 115200)
print('\nServer running')
try:
    rx_buffer = receive_simplified_with_timeout(ser,0.00175)
    print(rx_buffer)
finally:
    ser.close() 