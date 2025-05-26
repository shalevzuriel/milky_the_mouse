from microbit import*
from superbit import*
from machine import*
#Class ultrasonic sensors are the objects and you can measure distance.
class Ultra_Sensors:
    def __init__(self, trig, echo, timeout = 1000000):
        self.trig = trig
        self.echo = echo
        self.timeout = timeout
#measure distance in mm
    def distance_mm (self):
        self.trig.write_digital(1) #start pulse
        sleep(0.01)
        self.trig.write_digital(0) #end pulse
        time_measured  = time_pulse_us(self.echo, 1) #measure time of returned positive value of echo
        distance_mm = ((time_measured *0.343)/2) # calculate distance using speed of sound
        return distance_mm
    #measure distance in cm
    def distance_cm(self):
        return (self.distance_mm()/10)
            