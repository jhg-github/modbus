import serial
import time

ser = serial.Serial('/dev/ttyACM2', 115200, timeout=None)

ser.write(bytearray([1,3,0,126,0,2,164,19]))
# reply = ser.read(8)
# print(reply)
ser.close() 