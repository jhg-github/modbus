class ResponseTimeoutError(Exception):
    """
    Exception raised when the response timeout has expired without a reply
    """
    pass

class ReplyFrameNOKError(Exception):
    """
    Exception raised when the reply frame is NOK (CRC, ResponseTimeout)
    """
    pass