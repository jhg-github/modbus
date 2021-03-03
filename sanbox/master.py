import serial
import time

# from modbus_lib.modbus_serial import receive_for_master
from modbus_lib.modbus_serial import ModbusSerialLayer
import modbus_lib.exceptions as execps



def run():
    ser = serial.Serial('COM39', 115200)
    master = ModbusSerialLayer(ser, 1, 0.01)
    print('\nmaster running')
    try:
        # print()
        # tx_buffer = bytearray([1,3,0,126,0,2,164,19])
        # print('TX:', tx_buffer.hex())
        # ser.write(tx_buffer)
        # rx_buffer = receive_for_master(ser)
        # print('RX:', rx_buffer.hex())
        timeout_errors = 0
        frameNOK_errors = 0
        for total in range(100000):
            print()
            # time.sleep(1)
            try:  
                rx_buffer = master.send_request_unicast(1, bytearray([3,0,126,0,2]))
                print('RX: {:25}, total:{}, timeouts:{}, frameNOKs:{}'.format( rx_buffer.hex(), total, timeout_errors, frameNOK_errors) )
            except execps.ResponseTimeoutError:
                # print("ResponseTimeoutError exception catched!!!")
                timeout_errors += 1
                print('RX: {:25}, total:{}, timeouts:{}, frameNOKs:{} -- Timeout --'.format( rx_buffer.hex(), total, timeout_errors, frameNOK_errors) )
            except execps.ReplyFrameNOKError:
                # print("ReplyFrameNOKError exception catched!!!")
                frameNOK_errors += 1
                print('RX: {:25}, total:{}, timeouts:{}, frameNOKs:{} -- NOK --'.format( rx_buffer.hex(), total, timeout_errors, frameNOK_errors) )
    finally:
        ser.close() 