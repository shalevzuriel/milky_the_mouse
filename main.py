from microbit import *
from machine import*
import superbit as sb
from Ultra_Sensors import*
#available pins: 8, 12, 13, 14, 15, 16, (19,20 ?)
def motors(leftSpeed, rightSpeed): 
    intLeftSpeed = int(leftSpeed)
    intRightSpeed = int(rightSpeed)
    sb.motor_control(sb.M1, intLeftSpeed, 0) #left motor
    sb.motor_control(sb.M2, intLeftSpeed, 0) #left motor
    sb.motor_control(sb.M3, intRightSpeed, 0) #right motor
    sb.motor_control(sb.M4, intRightSpeed, 0) #right motor



motors(0,0)
sleep(2000)
leftSensor = Ultra_Sensors(pin12, pin13, 20)
rightSensor = Ultra_Sensors(pin1, pin2)
frontSensor = Ultra_Sensors(pin8, pin9)

STOPDISTANCE = 30 #Defined in mm
BASELINESPEED = 127
frontDistance = 10000
prevTime = running_time()
prevError = rightSensor.distance_mm()-leftSensor.distance_mm()
K_p = 0.9 #This is the coefficiant of e(t)
KD = 2 # This is the coefficiant of de/dt
ALPHA_E = 1   # Smoothing factor for error (0 < ALPHA < 1)
ALPHA_D = 0.8   # Smoothing factor for derivative
filtered_e_t = 0
filtered_der = 0

while(STOPDISTANCE < frontDistance):
    leftDistance = leftSensor.distance_mm()
    rightDistance = rightSensor.distance_mm()
    frontDistance = frontSensor.distance_mm()

    currentTime = running_time()
    e_t = rightDistance - leftDistance #This is e(t)
    filtered_e_t = (1 - ALPHA_E) * filtered_e_t + ALPHA_E * e_t
    de = filtered_e_t - prevError 
    dt = (currentTime-prevTime)/1000
    der = 0 if dt == 0 else de/dt
    filtered_der = (1 - ALPHA_D) * filtered_der + ALPHA_D * der
    u_t = filtered_e_t * K_p + filtered_der * KD
    left_speed = max(0, min(255, BASELINESPEED + u_t))
    right_speed = max(0, min(255, BASELINESPEED - u_t))
    motors(left_speed, right_speed)
    prevTime = currentTime
    prevError = filtered_e_t
    sleep(100)

motors(0,0)





