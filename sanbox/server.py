import serial
import time

from modbus_lib.modbus_serial import receive_for_server


def run():
    ser = serial.Serial('/dev/ttyACM0', 115200)
    print('\nServer running')
    try:
        while True:
            print()
            rx_buffer = receive_for_server(ser)
            print('RX:', rx_buffer.hex())
            tx_buffer = bytearray([1,3,4,204,205,62,76,69,9])
            ser.write(tx_buffer)
            print('TX:', tx_buffer.hex())
    finally:
        ser.close() 