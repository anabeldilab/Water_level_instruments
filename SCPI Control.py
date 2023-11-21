import serial

COM = 'COM4'
BAUD = 9600
ser = serial.Serial(COM, BAUD)

while (True):
    print("Enter command: ")
    command = input()
    command.strip()
    command += '\n'

    command_bytes = bytes(command, 'UTF-8')
    ser.write(command_bytes)

