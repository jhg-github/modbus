
def swap_bytes(word_val):
    """swap lsb and msb of a word"""
    msb = (word_val >> 8) & 0xFF
    lsb = word_val & 0xFF
    return (lsb << 8) + msb

def calc_crc(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos 
        for i in range(8):
            if ((crc & 1) != 0):
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    crc = swap_bytes(crc) # to match modbus format
    return crc


if __name__ == "__main__":
    data = bytearray([1,3,0,126,0,2])
    print(calc_crc(data))    
    data = bytearray([1,3,4,204,205,62,76])
    print(calc_crc(data))