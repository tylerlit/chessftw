import os

def convertToBinaryData(_filename):
    # Convert digital data to binary format
    with open(_filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def write_file(_data, _filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(_filename, 'wb') as file:
        file.write(_data)

def delete_file(_fileName):
    if os.path.exists(_fileName):
        os.remove(_fileName)
    else:
        print("The file does not exist")