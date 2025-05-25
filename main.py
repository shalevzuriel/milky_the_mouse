from microbit import *
from machine import*
from Ultra_Sensors import*
#available pins: 8, 12, 13, 14, 15, 16, (19,20 ?)
frontSensor = Ultra_Sensors(pin12, pin13)
rightSensor = Ultra_Sensors(pin1, pin2)
leftSensor = Ultra_Sensors(pin12, pin13)

print("test")
for i in range (100):
    distance = frontSensor.distance_mm()
    print(distance)
    sleep(10)
#sleep 10 works generally, tweaking can be in order
    
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