from microbit import *
from machine import*
import superbit as sb
from Ultra_Sensors import*
import radio
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
    #function to move forward, with correct type of PD when possible (using both sensors or just one) 
    def updateSensors(self):
        rightDistance = self.rightSensor.distance_mm()
        leftDistance = self.leftSensor.distance_mm()
        frontDistance = self.frontSensor.distance_mm()
        return (rightDistance, leftDistance, frontDistance)
    
    def moveBlock(self, stopDistance = 70): 

        BASELINE_SPEED = 127
        MADM = 200 #MADM = MAX_ACCEPTABLE_DISTANCE_MEASUREMENT
        MIDDLE_DISTANCE = 71
        ERROR_JUMP_THRESHOLD = 10
        frontDistance = 10000
        prevTime = running_time()
        K_p = 0.9 #This is the coefficiant of e(t)
        KD = 4 # This is the coefficiant of de/dt
        ALPHA_E = 1   # Smoothing factor for error (0 <= ALPHA <= 1)
        ALPHA_D = 0.8   # Smoothing factor for derivative
        filtered_e_t = 0
        filtered_der = 0

        #Now we define the initial Error before the loop
        rightDistance, leftDistance, frontDistance = self.updateSensors()
        if leftDistance<MADM and rightDistance <MADM: #case 1: both sensors are in range
            prevError = rightDistance-leftDistance 
        elif leftDistance>MADM and rightDistance<MADM: #case 2: PD using only right sensor
            prevError = 2*(rightDistance-MIDDLE_DISTANCE)
        elif leftDistance<MADM and rightDistance>MADM: #case 3: PD using only left sensor
            prevError = 2*(leftDistance-MIDDLE_DISTANCE)
        else:
            prevError = 1000 # defines not useable value in the case where no sesnsors can be used to prevent PD from being perfomed

        
        while(stopDistance < frontDistance):
            rightDistance, leftDistance, frontDistance = self.updateSensors()
            currentTime = running_time()
            radio.send("frontDistance " + str(frontDistance))
            radio.send("rightDistance " + str(rightDistance))
            radio.send("leftDistance " + str(leftDistance))
            #defining e(t) according to which PD you want to perform
            if leftDistance<MADM and rightDistance <MADM: #case 1: both sensors are in range
                e_t = rightDistance-leftDistance 
            elif leftDistance>MADM and rightDistance<MADM: #case 2: PD using only right sensor
                e_t = 2*(rightDistance-MIDDLE_DISTANCE)
            elif leftDistance<MADM and rightDistance>MADM: #case 3: PD using only left sensor
                e_t = 2*(leftDistance-MIDDLE_DISTANCE)
            else:
                e_t = 1000 #set e_t to an not useable value in case no sensor can be used. prevent PD from being performed.
            
            if abs(e_t-prevError)> ERROR_JUMP_THRESHOLD:
                self.motors(BASELINE_SPEED,BASELINE_SPEED)
                sleep(300)
            if abs(e_t)< 2*(MADM-MIDDLE_DISTANCE):
                filtered_e_t = (1 -  ALPHA_E) * filtered_e_t + ALPHA_E * e_t
                de = filtered_e_t - prevError 
                dt = (currentTime-prevTime)/1000 #change unites to seconds
                der = 0 if dt == 0 else de/dt #avoid deviding by zero 
                filtered_der = (1 - ALPHA_D) * filtered_der + ALPHA_D * der
                u_t = filtered_e_t * K_p + filtered_der * KD
                left_speed = max(0, min(255, BASELINE_SPEED + u_t)) #avoid out of bound error (max input to motors is 255)
                right_speed = max(0, min(255, BASELINE_SPEED - u_t))
                self.motors(left_speed, right_speed)
                prevTime = currentTime 
                prevError = filtered_e_t
                sleep(50)
            else:
                self.motors(BASELINE_SPEED, BASELINE_SPEED)
        self.motors(0,0)

    def turn(self, angleTime):
 #       if angleTime == 0: return 
        angleTimeSign = angleTime / abs(angleTime)
        initTime = running_time() 
        currentTime = 0
        while currentTime < abs(angleTime):
            frontDistance = self.frontSensor.distance_mm()
            self.motors(-200 * angleTimeSign, 200 * angleTimeSign)
            currentTime = running_time() - initTime
        self.motors(0,0)
        sleep(50)    


# radio.send("string" + str(num))