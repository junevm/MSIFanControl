import os

EC_IO_FILE = '/sys/kernel/debug/ec/ec0/io'

def write(BYTE, VALUE):
    try:
        with open(EC_IO_FILE, 'w+b') as file:
            file.seek(BYTE)
            file.write(bytes((VALUE,)))
    except PermissionError:
        print(f"Error: Permission denied writing to {EC_IO_FILE}. Are you running as root?")
    except FileNotFoundError:
        print(f"Error: {EC_IO_FILE} not found. Is the ec_sys module loaded?")

def read(BYTE, SIZE, FORMAT):
    VALUE = 0
    try:
        with open(EC_IO_FILE, 'r+b') as file:
            file.seek(BYTE)
            if SIZE == 1 and FORMAT == 0:
                VALUE = int(file.read(1).hex(), 16)
            elif SIZE == 1 and FORMAT == 1:
                VALUE = file.read(1).hex()
            elif SIZE == 2 and FORMAT == 0:
                VALUE = int(file.read(2).hex(), 16)
            elif SIZE == 2 and FORMAT == 1:
                VALUE = file.read(2).hex()
    except PermissionError:
        print(f"Error: Permission denied reading from {EC_IO_FILE}. Are you running as root?")
    except FileNotFoundError:
        print(f"Error: {EC_IO_FILE} not found. Is the ec_sys module loaded?")
    return VALUE
