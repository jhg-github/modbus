class ResponseTimeoutError(Exception):
    """
    Exception raised when the response timeout has expired without a reply
    """
    pass

class ReplyFrameNOKError(Exception):
    """
    Exception raised when the reply frame is NOK (CRC)
    """
    pass

class RequestSlaveIdError(Exception):
    """
    Exception raised when trying to make a request with an slave address out
    of valid range
    """

class RequestDataLengthError(Exception):
    """
    Exception raised when trying to make a request with wrong data length
    """

class ModbusExceptionIllegalFunction(Exception):
    """
    Exception code = 1
    Exception raised when the function code received in the query is not an 
    allowable action for the server. This may be because the function code is 
    only applicable to newer devices, and was not implemented in the unit 
    selected. It could also indicate that the server is in the wrong state to
    process a request of this type, for example because it is unconfigured and
    is being asked to return register values.
    """
    pass

class ModbusExceptionIllegalDataAddress(Exception):
    """
    Exception code = 2
    Exception raised when the data address received in the query is not an 
    allowable address for the server. More specifically, the combination of 
    reference number and transfer length is invalid. For a controller with 100 
    registers, the PDU addresses the first register as 0, and the last one as 
    99. If a request is submitted with a starting register address of 96 and a 
    quantity of registers of 4, then this request will successfully operate 
    (address-wise at least) on registers 96, 97, 98, 99. If a request is 
    submitted with a starting register address of 96 and a quantity of registers 
    of 5, then this request will fail with Exception Code 0x02 “Illegal Data 
    Address” since it attempts to operate on registers 96, 97, 98, 99 and 100, 
    and there is no register with address 100.
    """
    pass

class ModbusExceptionIllegalDataValue(Exception):
    """
    Exception code = 3
    Exception raised when a value contained in the query data field is not an 
    allowable value for server. This indicates a fault in the structure of the 
    remainder of a complex request, such as that the implied length is 
    incorrect. It specifically does NOT mean that a data item submitted for 
    storage in a register has a value outside the expectation of the application 
    program, since the MODBUS protocol is unaware of the significance of any 
    particular value of any particular register.
    """
    pass

class ModbusExceptionServerDeviceFailure(Exception):
    """
    Exception code = 4
    Exception raised when an unrecoverable error occurred while the server was 
    attempting to perform the requested action.
    """
    pass

class ModbusExceptionAcknowledge(Exception):
    """
    Exception code = 5
    Exception raised when a specialized use in conjunction with programming 
    commands.
    The server has accepted the request and is processing it, but a long duration 
    of time will be required to do so. This response is returned to prevent a 
    timeout error from occurring in the client. The client can next issue a Poll 
    Program Complete message to determine if processing is completed.
    """
    pass

class ModbusExceptionServerDeviceBusy(Exception):
    """
    Exception code = 6
    Exception raised when specialized use in conjunction with programming commands.
    The server is engaged in processing a long–duration program command. The client 
    should retransmit the message later when the server is free.
    """
    pass

class ModbusInvalidResponseLengthError(Exception):
    """
    Exception raised when the number of bytes received from slave is different
    that expected
    """

class ModbusUnknownException(Exception):
    """[summary]
    Exception raised when response function is neither the request function
    nor request function & 0x80
    """
    pass

