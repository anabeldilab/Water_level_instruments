import serial
import time

COM = 'COM5'
BAUD = 9600
ser = serial.Serial(COM, BAUD)
time.sleep(4)


CommandList = {
    'INC': 'TANK:LEVEL:INC',
    'DEC': 'TANK:LEVEL:DEC',
    'STOP': 'TANK:LEVEL:STOP',
    'UNITS?': 'TANK:LEVEL:UNITS?',
    'CHANGEUNITS': 'TANK:LEVEL:CHANGEUNITS',
    'TARGETWEIGHT?': 'TANK:LEVEL:TARGETWEIGHT?',
    'TARGETWEIGHT': 'TANK:LEVEL:TARGETWEIGHT',
    'TARE': 'TANK:LEVEL:TARE',
    'MAXWEIGHT' : 'TANK:LEVEL:MAXWEIGHT',
    'MAXWEIGHT?' : 'TANK:LEVEL:MAXWEIGHT?',
    'WATERLEVELREACHED?' : 'TANK:LEVEL:WATERLEVELREACHED?',
    'TOLERANCE' : 'TANK:LEVEL:TOLERANCE',
    'TOLERANCE?' : 'TANK:LEVEL:TOLERANCE?',
    'CALIBRATE' : 'TANK:LEVEL:CALIBRATE'
}


def arduino_SCPI(command_input):
    parts = command_input.split(' ', 1)
    short_command = parts[0]

    if short_command in CommandList:
        full_command = CommandList[short_command]

        if len(parts) > 1:
            full_command += ' ' + parts[1]

        full_command += '\n'
        command_bytes = bytes(full_command, 'UTF-8')
        ser.write(command_bytes)

        if (short_command.endswith('?')):
            #ser.flushInput()
            out = ser.readline().decode('UTF-8').strip()  # Lee una línea completa
            return out
    else:
        return "Invalid command"

'''
print("Getting units... ")
response = ''
response = arduino_SCPI('UNITS?')
if response is not None:
    print(">> " + response) 

print("Decrementing... ")
arduino_SCPI('INC')
time.sleep(10)

arduino_SCPI('STOP')

print("Getting units... ")
response = arduino_SCPI('UNITS?')
if response is not None:
    print(">> " + response) 

print("TARING... ")
arduino_SCPI('TARE')

time.sleep(2)

print("Getting units... ")
response = arduino_SCPI('UNITS?')
if response is not None:
    print(">> " + response) 


#print("Changing target weight... ")
#arduino
#_SCPI('TARGETWEIGHT' + response + str(500))

print("Changing units... ")
arduino_SCPI('CHANGEUNITS')

print("Getting units... ")
response = arduino_SCPI('UNITS?')
if response is not None:
    print(">> " + response) 

print("Getting units... ")
response = arduino_SCPI('UNITS?')
if response is not None:
    print(">> " + response) 

print("Changing units... ")
arduino_SCPI('CHANGEUNITS')


print("Getting units... ")
response = arduino_SCPI('UNITS?')
if response is not None:
    print(">> " + response) 

print("Changing units... ")
arduino_SCPI('CHANGEUNITS')

print("Getting units... ")
response = arduino_SCPI('UNITS?')
if response is not None:
    print(">> " + response) 


while (True):
    print("Enter command: ")
    command = input()
    command.strip()
    response = arduino
_SCPI(command)
    if response is not None:
        print(">> " + response) 


#time.sleep(5)

#arduino
#_SCPI("STOP")
'''