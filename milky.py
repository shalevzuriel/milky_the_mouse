from microbit import *
from machine import*
import superbit as sb
from Ultra_Sensors import*
#available pins: 8, 12, 13, 14, 15, 16, (19,20 ?)

class milky:
    def __init__(self, cell, orientation):
        self.cell = cell
        self.orientation = orientation
    
    def motors(self, leftSpeed, rightSpeed): #funciton to use motors. all left and all right motors work together
        intLeftSpeed = int(leftSpeed)
        intRightSpeed = int(rightSpeed)
        sb.motor_control(sb.M1, intLeftSpeed, 0) #left motor
        sb.motor_control(sb.M2, intLeftSpeed, 0) #left motor
        sb.motor_control(sb.M3, intRightSpeed, 0) #right motor
        sb.motor_control(sb.M4, intRightSpeed, 0) #right motor

    def moveBlock(self, stopDistance = 70): #function to move forward, with PD when possible (abs(et)>280), until close enough to a wall     
        leftSensor = Ultra_Sensors(pin12, pin13, 20)
        rightSensor = Ultra_Sensors(pin1, pin2)
        frontSensor = Ultra_Sensors(pin8, pin9)

        BASELINESPEED = 127
        frontDistance = 10000
        prevTime = running_time()
        prevError = rightSensor.distance_mm()-leftSensor.distance_mm()
        K_p = 0.9 #This is the coefficiant of e(t)
        KD = 2 # This is the coefficiant of de/dt
        ALPHA_E = 1   # Smoothing factor for error (0 <= ALPHA <= 1)
        ALPHA_D = 0.8   # Smoothing factor for derivative
        filtered_e_t = 0
        filtered_der = 0

        while(stopDistance < frontDistance):
            leftDistance = leftSensor.distance_mm()
            rightDistance = rightSensor.distance_mm()
            frontDistance = frontSensor.distance_mm()

            currentTime = running_time()
            e_t = rightDistance - leftDistance #This is e(t)
            if abs(e_t)<280:
                filtered_e_t = (1 - ALPHA_E) * filtered_e_t + ALPHA_E * e_t
                de = filtered_e_t - prevError 
                dt = (currentTime-prevTime)/1000
                der = 0 if dt == 0 else de/dt
                filtered_der = (1 - ALPHA_D) * filtered_der + ALPHA_D * der
                u_t = filtered_e_t * K_p + filtered_der * KD
                left_speed = max(0, min(255, BASELINESPEED + u_t))
                right_speed = max(0, min(255, BASELINESPEED - u_t))
                self.motors(left_speed, right_speed)
                prevTime = currentTime
                prevError = filtered_e_t
                sleep(100)
            else:
                self.motors(127, 127)
        self.motors(0,0)





