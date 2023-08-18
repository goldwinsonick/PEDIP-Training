def calcChecksum(byteArr):
    print(byteArr)
    checksum = 0
    for byte in byteArr:
        checksum ^= byte
    # return checksum.to_bytes(2, byteorder="little")
    return checksum
b = bytearray()
b.extend(map(ord, "Hello"))
print(calcChecksum(b))
