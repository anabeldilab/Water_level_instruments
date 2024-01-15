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