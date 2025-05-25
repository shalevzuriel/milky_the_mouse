from microbit import *
from machine import*
import microbit
import superbit

display.show("HI")
print("test")
while True:
    pin9.write_digital(1)
    sleep(0.001)
    pin9.write_digital(0)
    time = time_pulse_us(pin10, 1)
    distance = ((time*0.343)/2)/10
    print(distance)
    sleep(100)

    
    
''''
while True:
    superbit.motor_control(superbit.M1, 255, 0)
    superbit.motor_control(superbit.M2, 255, 0)
    superbit.motor_control(superbit.M3, 255, 0)
    superbit.motor_control(superbit.M4, 255, 0)
    microbit.sleep(1000)

    superbit.motor_control(superbit.M1, 0, 0)
    superbit.motor_control(superbit.M2, 0, 0)
    superbit.motor_control(superbit.M3, 0, 0)
    superbit.motor_control(superbit.M4, 0, 0)
    microbit.sleep(1000)

    superbit.motor_control(superbit.M1, -255, 0)
    superbit.motor_control(superbit.M2, -255, 0)
    superbit.motor_control(superbit.M3, -255, 0)
    superbit.motor_control(superbit.M4, -255, 0)
    microbit.sleep(1000)
'''