import serial
import time

COM = 'COM6'
BAUD = 9600
ser = serial.Serial(COM, BAUD)

while (True):
    print("Enter command: ")
    command = input()
    command.strip()
    command += '\n'

    command_bytes = bytes(command, 'UTF-8')
    ser.write(command_bytes)

    time.sleep(1)

    out = ''
    while ser.inWaiting() > 0:
        out += ser.read(2).decode('UTF-8')
    if out != '':
        print(">> " + out)



    




