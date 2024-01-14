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
}


def SCPI_Arduino(command_input):
    # Divide el comando y los parámetros adicionales
    parts = command_input.split(' ', 1)
    short_command = parts[0]

    # Verifica si el comando abreviado es válido
    if short_command in CommandList:
        # Convierte el comando completo a bytes
        full_command = CommandList[short_command]

        # Si hay parámetros adicionales, añádelos al comando
        if len(parts) > 1:
            full_command += ' ' + parts[1]

        full_command += '\n'
        command_bytes = bytes(full_command, 'UTF-8')
        ser.write(command_bytes)

        if (short_command.endswith('?')):
            out = ser.readline().decode('UTF-8').strip()  # Lee una línea completa
            return out
    else:
        return "Invalid command"

'''
print("Getting units... ")
response = ''
response = SCPI_Arduino('UNITS?')
if response is not None:
    print(">> " + response) 

print("Decrementing... ")
SCPI_Arduino('INC')
time.sleep(10)

SCPI_Arduino('STOP')

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


#print("Changing target weight... ")
#SCPI_Arduino('TARGETWEIGHT' + response + str(500))

print("Changing units... ")
SCPI_Arduino('CHANGEUNITS')

print("Getting units... ")
response = SCPI_Arduino('UNITS?')
if response is not None:
    print(">> " + response) 

print("Getting units... ")
response = SCPI_Arduino('UNITS?')
if response is not None:
    print(">> " + response) 

print("Changing units... ")
SCPI_Arduino('CHANGEUNITS')


print("Getting units... ")
response = SCPI_Arduino('UNITS?')
if response is not None:
    print(">> " + response) 

print("Changing units... ")
SCPI_Arduino('CHANGEUNITS')

print("Getting units... ")
response = SCPI_Arduino('UNITS?')
if response is not None:
    print(">> " + response) 


while (True):
    print("Enter command: ")
    command = input()
    command.strip()
    response = SCPI_Arduino(command)
    if response is not None:
        print(">> " + response) 


#time.sleep(5)

#SCPI_Arduino("STOP")
'''