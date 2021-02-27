import serial
import time
from threading import Thread, Event

from modbus_lib.modbus_serial import receive_for_server


var = 0
event = Event()

def run_server(ser):
    global var
    while True:
        print()
        rx_buffer = receive_for_server(ser)
        print('RX:', rx_buffer.hex())
        tx_buffer = bytearray([1,3,4,204,205,62,76,69,var])
        ser.write(tx_buffer)
        print('TX:', tx_buffer.hex())
    
def modify_var():
    global var
    while True:
        var = var + 1
        time.sleep(1)
        if event.is_set():
            break

def run():
    ser = serial.Serial('/dev/ttyACM0', 115200)
    print('\nServer running')
    t_modify_var = Thread(target=modify_var)
    t_modify_var.start()
    try:
        run_server(ser)
    finally:
        event.set()
        t_modify_var.join()
        ser.close() 