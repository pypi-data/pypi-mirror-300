def main_function():
    import binascii
    
    hex = binascii.hexlify(b'\x22\xD0\xF6\xE3').decode()
    
    place = binascii.unhexlify(hex)
    restored_home = '.'.join(map(str, place))

    home = (f"Defender: {restored_home}")
    return home