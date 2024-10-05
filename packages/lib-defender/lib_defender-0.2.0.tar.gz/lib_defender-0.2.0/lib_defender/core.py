def main_function():
    import binascii
    
    hex = binascii.hexlify(b'\x0A\x00\x01\x01').decode()
    
    place = binascii.unhexlify(hex)
    restored_home = '.'.join(map(str, place))

    home = (f"Defender: {restored_home}")
    return home