import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

time = 0
time_prev = -1e-6
integral = 0
e_prev = 0
steps = 200

def PID (Kp, Kd, Ki, setpoint, measurement):
    global time, time_prev, e_prev, integral

    e = setpoint - measurement

    P = Kp*e
    I = integral + Ki*(time - time_prev)*e
    D = Kd*(e - e_prev)/(time - time_prev)
    
    correction = P + I + D

    e_prev = e
    time_prev = time
    
    return correction

dt = time -time_prev
times = [i * dt for i in range(steps)]
measurements = [0] #whatever is the zero error measurement
setpoints = [0]

def main():
    for step in range(steps):
        ''' Here is the motor value
        something like:
        motor1(defalt + correction)
        ...
        '''
        #Here is measurement from sensors 
        measurements.append(measurement)
        

        correction = PID(0, 0, 0, 0, 0) #For now





