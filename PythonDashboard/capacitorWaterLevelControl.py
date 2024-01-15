import numpy as np
from scipy.optimize import root_scalar
from redpitaya_instrument import RC_circuit_value
from arduino_scpi import arduino_SCPI

def controlWaterLevel(optimized_rc_params):
    from app import global_max_weight, global_target_weight
    capacitorValue = RC_circuit_value()
    capacitorWeight = find_weight_for_rc(capacitorValue, *optimized_rc_params)
    capacitorWaterLevelReached = False
    
    if (capacitorWeight is None or global_max_weight is None):
        print("Error al encontrar el peso para el valor RC")
        return capacitorWaterLevelReached
    global_max_weight = float(global_max_weight)
    if (isWeightReached(capacitorWeight) or capacitorWeight >= global_max_weight):
        waterLevelReached()
        capacitorWaterLevelReached = True
    elif (capacitorWeight < global_target_weight):
        fillContainer()
    elif (capacitorWeight > global_target_weight): 
        emptyContainer()
    return capacitorWaterLevelReached
  

def isWeightReached(capacitorWeight):
    from app import global_hysteresis, global_target_weight
    return capacitorWeight >= global_target_weight - global_hysteresis and capacitorWeight <= global_target_weight + global_hysteresis


def waterLevelReached():
    arduino_SCPI("STOP")


def fillContainer():
    arduino_SCPI("INC")


def emptyContainer():
    arduino_SCPI("DEC")

# Definición de la función de ajuste exponencial
def exp_func(x, a, b, c):
    return a * np.exp(-b * x) + c


def find_weight_for_rc(y, a, b, c):
    func = lambda x: exp_func(x, a, b, c) - y
    try:
        return root_scalar(func, method='newton', x0=0).root
    except Exception as e:
        print("Error al encontrar el peso para el valor RC:", e)
        return None