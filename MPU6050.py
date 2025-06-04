from microbit import *

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.i2c.write(self.addr, bytes([0x6B, 0]))  # Wake up MPU6050

    def read_raw_data(self, reg):
        # Write the register address to tell MPU6050 what to read
        self.i2c.write(self.addr, bytes([reg]))
        data = self.i2c.read(self.addr, 2)  # Read two bytes
        value = (data[0] << 8) | data[1]
        if value > 32767:
            value -= 65536
        return value


    def get_accel(self):
        x = self.read_raw_data(0x3B)
        y = self.read_raw_data(0x3D)
        z = self.read_raw_data(0x3F)
        return (x, y, z)

    def get_gyro(self):
        x = self.read_raw_data(0x43)
        y = self.read_raw_data(0x45)
        z = self.read_raw_data(0x47)
        return (x, y, z)
    
    def calibrate(self, samples=100):
        print("calibrating")
        total = 0
        for i in range(samples):
            _, _, gz = self.get_gyro()
            total += gz
            sleep(10)
        return total / samples
    

# Here is example usage code
# This code needs to be initiated in main.py - it defines the i2c and the gyro
i2c.init(freq=400000, sda=pin20, scl=pin19)
mpu = MPU6050(i2c) 
# This method is used to turn x degrees, if degrees is positive we turn counter-clockwise (right hand system)
# We also need to put the gyro (in this case we defined it "mpu"). 
def turn(degrees, gyro, calibrating_steps=100, low_pass_coefficiant=0.2):
    prevTime = running_time()
    gyro_bias = mpu.calibrate(calibrating_steps) #find the gyro bias
    alpha = low_pass_coefficiant #coefficiant for low-pass filtering
    gyro_angle = 0 #initialize angle
    prev_gz_dps = 0 #dps - dgrees per second
    while abs(gyro_angle) < degrees:
        
        """
        Here we move the motors so that we turn in the right direction. 
        If degrees > 0 we turn counter-clockwise
        If degrees < 0 we turn clockwise
        That is when the red led is pointed up (where all the components are)
        """

        _, _, gz = gyro.get_gyro()
        gz_dps = (gz - gyro_bias) / 131.0 # degrees per second, remove bias from measurement

        currentTime = running_time()
        dt = (currentTime - prevTime) / 1000

        filtered_gz = alpha * gz_dps + (1-alpha) * prev_gz_dps #filtering using low-pass filtering
        gyro_angle += filtered_gz * dt #summing chang in angle over time

        prevTime = currentTime #updating prev time
        prev_gz_dps = filtered_gz

        print("angle: ", gyro_angle) #no real need for printing, just for testing
        sleep(100) #arbitrary, could change

