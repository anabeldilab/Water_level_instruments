import sys
import time
import redpitaya_scpi as scpi
import matplotlib.pyplot as plot

IP = "192.168.1.48"
rp_s = scpi.scpi(IP)

wave_form = 'sine'
freq = 2000
ampl = 1
min_level = 0.013871513306939288

def set_rc_circuit_frequency(newFreq):
    global freq
    freq = newFreq

def RC_circuit_value():
    # Generation
    rp_s.tx_txt('GEN:RST')
    rp_s.tx_txt('ACQ:RST')

    rp_s.tx_txt('SOUR1:FUNC ' + str(wave_form).upper())
    rp_s.tx_txt('SOUR1:FREQ:FIX ' + str(freq))
    rp_s.tx_txt('SOUR1:VOLT ' + str(ampl))

    rp_s.tx_txt('OUTPUT1:STATE ON')
    rp_s.tx_txt('SOUR1:TRIG:INT')
    rp_s.tx_txt('ACQ:DEC 16')

    rp_s.tx_txt('ACQ:START')
    time.sleep(1)
    rp_s.tx_txt('ACQ:TRIG NOW')


    ## UNIFIED OS
    while 1:
        rp_s.tx_txt('ACQ:TRIG:FILL?')
        if rp_s.rx_txt() == '1':
            break

    rp_s.tx_txt('ACQ:SOUR1:DATA?')
    buff_string = rp_s.rx_txt()
    buff_string = buff_string.strip('{}\n\r').replace("  ", "").split(',')
    buff = list(map(float, buff_string))

    buff = [val - sum(buff) / len(buff) for val in buff]

    abs_buff = [abs(val) for val in buff]

    avg_read_sine = sum(abs_buff) / len(abs_buff)

    attenuation = avg_read_sine / min_level

#print(attenuation)


#plot.plot(buff)
#plot.ylabel('Voltage')
#plot.show()
    return attenuation

