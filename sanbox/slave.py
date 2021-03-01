import serial
import time
from threading import Thread, Event

from modbus_lib.modbus_serial import receive_for_slave


var = 0
event = Event()

def run_slave(ser):
    global var
    while True:
        print()
        rx_buffer = receive_for_slave(ser)
        print('RX:', rx_buffer.hex())
        time.sleep(3)
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
    ser = serial.Serial('COM38', 115200)
    print('\nslave running')
    t_modify_var = Thread(target=modify_var)
    t_modify_var.start()
    try:
        run_slave(ser)
    finally:
        event.set()
        t_modify_var.join()
        ser.close() 