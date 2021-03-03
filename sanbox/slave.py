import serial
import time
from threading import Thread, Event

from modbus_lib.modbus_serial import ModbusSerialLayer


var = 0
event = Event()

def run_slave(slave):
    global var

    while True:
        print()
        rx_buffer = slave.receive_for_slave()
        print('RX:', rx_buffer.hex())
        tx_buffer = bytearray([1,3,4,204,205,62,76,69,9])
        slave.send_frame(tx_buffer)
        # print('TX:', tx_buffer.hex())
    
# def modify_var():
#     global var
#     while True:
#         var = var + 1
#         time.sleep(1)
#         if event.is_set():
#             break

def run():
    ser = serial.Serial('COM38', 115200)
    slave = ModbusSerialLayer(ser, 1, 0.01)
    print('\nslave running')
    # t_modify_var = Thread(target=modify_var)
    # t_modify_var.start()
    try:
        run_slave(slave)
    finally:
        # event.set()
        # t_modify_var.join()
        ser.close() 