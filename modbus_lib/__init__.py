import logging

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger("modbus_lib")
c_handler = logging.StreamHandler()
c_format = logging.Formatter("%(asctime)s\t%(levelname)s\t%(message)s\t%(module)s.%(funcName)s\t%(threadName)s")
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)
