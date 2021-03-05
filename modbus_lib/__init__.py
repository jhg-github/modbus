import logging

logging.root.setLevel(logging.DEBUG)
logger = logging.getLogger("modbus_lib")
c_handler = logging.StreamHandler()
c_format = logging.Formatter("%(asctime)s\t|\t%(levelname)s\t|\t%(message)s\t|\t%(module)s.%(funcName)s\t|\t%(threadName)s")
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)
