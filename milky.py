from microbit import *
from machine import*
import superbit as sb
from Ultra_Sensors import*
#available pins: 8, 12, 13, 14, 15, 16, (19,20 ?)

class milky:
    def __init__(self, cell, orientation, rightSensor, leftSensor, frontSensor):
        self.cell = cell
        self.orientation = orientation
        self.rightSensor = rightSensor
        self.frontSensor = frontSensor
        self.leftSensor = leftSensor
    
    def motors(self, leftSpeed, rightSpeed): #funciton to use motors. all left and all right motors work together
        intLeftSpeed = int(leftSpeed)
        intRightSpeed = int(rightSpeed)
        sb.motor_control(sb.M1, intLeftSpeed, 0) #left motor
        sb.motor_control(sb.M2, intLeftSpeed, 0) #left motor
        sb.motor_control(sb.M3, intRightSpeed, 0) #right motor
        sb.motor_control(sb.M4, intRightSpeed, 0) #right motor

    def moveBlock(self, stopDistance = 70): #function to move forward, with PD when possible (abs(et)>280), until close enough to a wall     

        BASELINESPEED = 127
        frontDistance = 10000
        prevTime = running_time()
        prevError = self.rightSensor.distance_mm()-self.leftSensor.distance_mm()
        K_p = 0.9 #This is the coefficiant of e(t)
        KD = 4 # This is the coefficiant of de/dt
        ALPHA_E = 1   # Smoothing factor for error (0 <= ALPHA <= 1)
        ALPHA_D = 0.8   # Smoothing factor for derivative
        filtered_e_t = 0
        filtered_der = 0

        while(stopDistance < frontDistance):
            #leftDistance = self.leftSensor.distance_mm()
            #print(leftDistance)
            rightDistance = self.rightSensor.distance_mm()
            frontDistance = self.frontSensor.distance_mm()
            print(rightDistance)

            currentTime = running_time()
            e_t = 2*(rightDistance - 75) #This is e(t)
            if abs(e_t-prevError)> 10:
                self.motors(127,127)
                sleep(300)
            if abs(e_t)<180:
                filtered_e_t = (1 -  ALPHA_E) * filtered_e_t + ALPHA_E * e_t
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
                sleep(50)
            else:
                self.motors(127, 127)
        self.motors(0,0)

    def turn(self, angleTime):
        frontDistance = self.frontSensor.distance_mm()
        angleTimeSign = angleTime / abs(angleTime)
        initTime = running_time() 
        currentTime = 0
        while currentTime < abs(angleTime) and frontDistance > 30:
            frontDistance = self.frontSensor.distance_mm()
            self.motors(-200 * angleTimeSign, 200 * angleTimeSign)
            currentTime = running_time() - initTime
            print(currentTime)
        self.motors(0,0)
        sleep(50)    



'''
    def turn(self, degrees, calibrating_steps=100, low_pass_coefficiant=0.2):
        prevTime = running_time()
        gyro_bias = self.gyro.calibrate(calibrating_steps) #find the gyro bias
        alpha = low_pass_coefficiant #coefficiant for low-pass filtering
        gyro_angle = 0 #initialize angle
        prev_gz_dps = 0 #dps - dgrees per second
        while abs(gyro_angle) < degrees:
            self.motors(-120*degrees/abs(degrees), 120*degrees/abs(degrees))

            _, _, gz = self.gyro.get_gyro()
            gz_dps = (gz - gyro_bias) / 131.0 # degrees per second, remove bias from measurement

            currentTime = running_time()
            dt = (currentTime - prevTime) / 1000

            filtered_gz = alpha * gz_dps + (1-alpha) * prev_gz_dps #filtering using low-pass filtering
            gyro_angle += filtered_gz * dt #summing chang in angle over time

            prevTime = currentTime #updating prev time
            prev_gz_dps = filtered_gz

            print("angle: ", gyro_angle) #no real need for printing, just for testing
            sleep(100) #arbitrary, could change
'''


