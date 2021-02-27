import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0)

elapsed_list=[]
data_list=[]
while True:
    start = time.time()
    data = ser.read(1)
    elapsed = time.time()-start
    if data:
        elapsed_list.append(elapsed)
        data_list.append(data)
        print("elapsed = ", elapsed)
        if data == bytes('0', 'utf-8'):
            break
print('average time =', sum(elapsed_list) / len(elapsed_list))
print('data =', data)
ser.close() 