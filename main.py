from microbit import *
from machine import*
import superbit as sb
from Ultra_Sensors import*
from milky import*
import radio
#from MPU6050 import*
#available pins: 8, 12, 13, 14, 15, 16, (19,20 ?)

radio.on()
radio.config(group=1)
BLOCK_LENGTH = 262 #mm
TURN_RIGHT_TIME = -1450 #check real values
TURN_LEFT_TIME = 1400
BASE_STOP = 90
leftSensor = Ultra_Sensors(pin12, pin13)
rightSensor = Ultra_Sensors(pin1, pin2)
frontSensor = Ultra_Sensors(pin8, pin9)

sleep(300)
robot = milky(leftSensor=leftSensor, rightSensor=rightSensor, frontSensor=frontSensor, orientation=0, cell=pin16)

robot.moveBlock(BASE_STOP)
radio.send("1 Finished move command")
robot.turn(TURN_LEFT_TIME)
radio.send("1 Finished turn command")
robot.moveBlock(BASE_STOP + 2*BLOCK_LENGTH)
radio.send("2 Finished move command")
robot.turn(TURN_LEFT_TIME)
radio.send("2 Finished turn command")
robot.moveBlock(BASE_STOP)
radio.send("3 Finished move command")
robot.turn(TURN_RIGHT_TIME)
radio.send("3 Finished turn command")
robot.moveBlock(BASE_STOP)
radio.send("4 Finished move command")
robot.turn(TURN_LEFT_TIME)
radio.send("1 Finished turn command")
robot.moveBlock(BASE_STOP + 2 * BLOCK_LENGTH)
radio.send("5 Finished move command")
robot.turn(TURN_LEFT_TIME)
radio.send("5 Finished turn command")
robot.moveBlock(BASE_STOP + BLOCK_LENGTH)
radio.send("6 Finished move command")

'''

-------------------------------------------


leftSensor = Ultra_Sensors(pin12, pin13)
rightSensor = Ultra_Sensors(pin1, pin2)
frontSensor = Ultra_Sensors(pin8, pin9)
#i2c.init(freq=400000, sda=pin20, scl=pin19)
#gyro = MPU6050(i2c) 

robot = milky(leftSensor=leftSensor, rightSensor=rightSensor, frontSensor=frontSensor, orientation=0, cell=pin16)

robot.turn(1500)
robot.moveBlock()
robot.turn(1500)
robot.moveBlock()
robot.turn(1500)
robot.moveBlock()
-------------------------------------------
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

'''



