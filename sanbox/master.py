import serial
import time
import logging

# from modbus_lib.modbus_serial import receive_for_master
from modbus_lib.modbus_serial import ModbusSerialLayer
from modbus_lib.modbus_master import ModbusMaster
import modbus_lib.exceptions as execps
from modbus_lib.utils import init_logger


def test_ReadSingleRegister(mod_master):
    response = mod_master.read_holding_registers(1, 0, 1)
    return response

def test_ReadMultipleRegisters(mod_master):
    response = mod_master.read_holding_registers(1, 0, 125)
    return response

def test_ReadMultipleRegisters_Xtimes(mod_master):
    frames_nok = 0
    timeouts = 0
    for i in range(10000):
        try:
            response = test_ReadMultipleRegisters(mod_master)
        except execps.ReplyFrameNOKError:
            frames_nok += 1
        except execps.ResponseTimeoutError:
            timeouts += 1
        finally:
            print(f'{i+1} TOT | {frames_nok} NOK | {timeouts} TOUT')

def test_WriteMultipleRegisters(mod_master):
    mod_master.write_multiple_registers(1, 1, 2, bytearray([1,2,3,4]))    


def test_ForceRequestSlaveIdError(mod_master):
    response = mod_master.read_holding_registers(248, 107, 3)
    return response

def test_ForceWriteNumberRegistersError(mod_master):
    response = mod_master.write_multiple_registers(1, 1, 124, bytearray())
    return response

def test_ForceWriteDataLengthError(mod_master):
    mod_master.write_multiple_registers(1, 1, 2, bytearray([1,2,3,4,5]))    

def run():
    # ser = serial.Serial('COM39', 115200)
    # ser = serial.Serial('COM28', 115200)
    ser = serial.Serial('COM28', 9600, parity='E')
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    # ser.set_buffer_size(rx_size = 12800, tx_size = 12800)
    mod_master = ModbusMaster(ser, 1, 0.05,True,logging.DEBUG)
    print('\nmaster running')
    try:  
        # response = test_ReadSingleRegister(mod_master)
        # response = test_ReadMultipleRegisters(mod_master)
        # test_WriteMultipleRegisters(mod_master)
        # response = test_ForceRequestSlaveIdError(mod_master)
        # response = test_ForceWriteNumberRegistersError(mod_master)
        # response = test_ForceWriteDataLengthError(mod_master)
        mod_master.write_multiple_registers(1, 1300, 4, bytearray([204,205,61,204,204,205,63,140]))   #writes to 7060CO
        # print('Response:', response.hex())
        # test_ReadMultipleRegisters_Xtimes(mod_master)
        


    except Exception as exc:
        print(str(exc))
    finally:
        ser.close() 

        
