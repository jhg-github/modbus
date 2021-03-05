import serial
import time
from threading import Thread, Event
import struct

from modbus_lib.modbus_serial import ModbusSerialLayer


var = 0
event = Event()
# def modify_var():
#     global var
#     while True:
#         var = var + 1
#         time.sleep(1)
#         if event.is_set():
#             break


def test_aux_CreateModbusException(rx_buffer, exception_code):
    slave_id = rx_buffer[0]
    function = rx_buffer[1] | 0x80
    pdu = bytearray([function, exception_code ])
    response = ModbusSerialLayer.create_serial_pdu(slave_id, pdu)
    return response

def test_ReadSingleHoldingRegister(rx_buffer):
    slave_id = rx_buffer[0]
    function = rx_buffer[1]
    starting_address = struct.unpack('>H',rx_buffer[2:4])[0]
    data = struct.pack('>H',starting_address+1000)
    pdu = bytearray([function, 2 ]) + data
    response = ModbusSerialLayer.create_serial_pdu(slave_id, pdu)
    return response

def test_ForceResponseTimeoutError(rx_buffer):
    time.sleep(2)
    return bytearray([1,3,4,204,205,62,76,69,9])

def test_ForceReplyFrameNOKError(rx_buffer):
    return bytearray([1,3,4,204,205,62,76,69,1])

def test_ForceModbusExceptionIllegalFunction(rx_buffer):
    return test_aux_CreateModbusException(rx_buffer, 1)

def test_ForceModbusExceptionIllegalDataAddress(rx_buffer):
    return test_aux_CreateModbusException(rx_buffer,2)

def test_ForceModbusExceptionIllegalDataValue(rx_buffer):
    return test_aux_CreateModbusException(rx_buffer,3)

def test_ForceModbusExceptionServerDeviceFailure(rx_buffer):
    return test_aux_CreateModbusException(rx_buffer,4)

def test_ForceModbusExceptionAcknowledge(rx_buffer):
    return test_aux_CreateModbusException(rx_buffer,5)

def test_ForceModbusExceptionServerDeviceBusy(rx_buffer):
    return test_aux_CreateModbusException(rx_buffer,6)

def test_ForceModbusInvalidResponseLengthError(rx_buffer):
    slave_id = rx_buffer[0]
    function = rx_buffer[1]
    starting_address = struct.unpack('>H',rx_buffer[2:4])[0]
    data = struct.pack('>HH',starting_address+1000,starting_address+1000)
    pdu = bytearray([function, 2 ]) + data
    response = ModbusSerialLayer.create_serial_pdu(slave_id, pdu)
    return response

def test_ForceModbusUnknownException(rx_buffer):
    slave_id = rx_buffer[0]
    function = rx_buffer[1]+1
    starting_address = struct.unpack('>H',rx_buffer[2:4])[0]
    data = struct.pack('>H',starting_address+1000)
    pdu = bytearray([function, 2 ]) + data
    response = ModbusSerialLayer.create_serial_pdu(slave_id, pdu)
    return response


def run_slave(slave):
    # global var
    while True:
        print()
        rx_buffer = slave.receive_for_slave()

        # tx_buffer = test_ReadSingleHoldingRegister(rx_buffer)
        # tx_buffer = test_ForceResponseTimeoutError(rx_buffer)
        # tx_buffer = test_ForceReplyFrameNOKError(rx_buffer)
        # tx_buffer = test_ForceModbusExceptionIllegalFunction(rx_buffer)
        # tx_buffer = test_ForceModbusExceptionIllegalDataAddress(rx_buffer)
        # tx_buffer = test_ForceModbusExceptionIllegalDataValue(rx_buffer)
        # tx_buffer = test_ForceModbusExceptionServerDeviceFailure(rx_buffer)
        # tx_buffer = test_ForceModbusExceptionAcknowledge(rx_buffer)
        # tx_buffer = test_ForceModbusExceptionServerDeviceBusy(rx_buffer)
        # tx_buffer = test_ForceModbusInvalidResponseLengthError(rx_buffer)
        tx_buffer = test_ForceModbusUnknownException(rx_buffer)
        
        slave.send_frame(tx_buffer)
    


def run():
    ser = serial.Serial('COM38', 115200)
    slave = ModbusSerialLayer(ser, 1, 0.01)
    print('\nslave running')
    # t_modify_var = Thread(target=modify_var)
    # t_modify_var.start()
    try:
        run_slave(slave)
    except Exception as exc:
        print(str(exc))
    finally:
        # event.set()
        # t_modify_var.join()
        ser.close() 