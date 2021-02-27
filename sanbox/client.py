import serial
import time

from modbus_lib.modbus_serial import receive_for_client


def run():
    ser = serial.Serial('/dev/ttyACM2', 115200)
    print('\nClient running')
    try:
        print()
        tx_buffer = bytearray([1,3,0,126,0,2,164,19])
        print('TX:', tx_buffer.hex())
        ser.write(tx_buffer)
        rx_buffer = receive_for_client(ser)
        print('RX:', rx_buffer.hex())
    finally:
        ser.close() 