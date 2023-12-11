import serial
import time

COM = 'COM4'
BAUD = 9600
ser = serial.Serial(COM, BAUD)
time.sleep(4)


CommandList = {
    'INC': 'TANK:LEVEL:INC',
    'DEC': 'TANK:LEVEL:DEC',
    'STOP': 'TANK:LEVEL:STOP',
    'UNITS?': 'TANK:LEVEL:UNITS?',
    'TARGETWEIGHT?': 'TANK:LEVEL:TARGETWEIGHT?',
    'TARGETWEIGHT': 'TANK:LEVEL:TARGETWEIGHT',
    'TARE': 'TANK:LEVEL:TARE',

}


def SCPI_Arduino(short_command):
    # Check if the shorthand command is valid
    if short_command in CommandList:
        # Convert the full command to bytes 
        command = CommandList[short_command]
        command += '\n'

        command_bytes = bytes(command, 'UTF-8')
        ser.write(command_bytes)

        time.sleep(1)

        out = ''
        while ser.inWaiting() > 0:
            out += ser.read(1).decode('UTF-8')
        if out != '':
            return out
    else:
        return "Invalid command"

print("Getting units... ")
response = ''
response = SCPI_Arduino('UNITS?')
if response is not None:
    print(">> " + response) 

print("Decrementing... ")
SCPI_Arduino('INC')
time.sleep(10)

print("Getting units... ")
response = SCPI_Arduino('UNITS?')
if response is not None:
    print(">> " + response) 

print("TARING... ")
SCPI_Arduino('TARE')

time.sleep(2)

print("Getting units... ")
response = SCPI_Arduino('UNITS?')
if response is not None:
    print(">> " + response) 


print("Stopping... ")
SCPI_Arduino('STOP')

#time.sleep(5)

#SCPI_Arduino("STOP")
