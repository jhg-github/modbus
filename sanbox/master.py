import serial
import time

# from modbus_lib.modbus_serial import receive_for_master
from modbus_lib.modbus_serial import send_request_unicast
import modbus_lib.exceptions as execps


def run():
    ser = serial.Serial('COM39', 115200)
    print('\nmaster running')
    try:
        # print()
        # tx_buffer = bytearray([1,3,0,126,0,2,164,19])
        # print('TX:', tx_buffer.hex())
        # ser.write(tx_buffer)
        # rx_buffer = receive_for_master(ser)
        # print('RX:', rx_buffer.hex())
        print()
        try:  
            rx_buffer = send_request_unicast(ser, 1, bytearray([3,0,126,0,2]))
        except execps.ResponseTimeoutError:
            print("ResponseTimeoutError exception catched!!!")
        except execps.ReplyFrameNOKError:
            print("ReplyFrameNOKError exception catched!!!")
        print('RX:', rx_buffer.hex())
    finally:
        ser.close() 