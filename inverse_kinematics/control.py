
"""PLANS:
Multithreading
Looking RPI GPIO PWM
"""

import time
import RPi.GPIO as GPIO
import math
from threading import Thread


class Stepper(object):
    def __init__(self, micro_steps, start_high, start_low, start_rot):
        # Set mode on GPIO.
        GPIO.setmode(GPIO.BCM)

        # pins [steps, dir]
        self.higher = [17, 4]
        self.lower = [22, 27]
        self.rot = [6, 5]
        self.claw = [5,6,12,13]

        # Micro steps pins on DRV8825
        self.M_0 = 13
        GPIO.setup(self.M_0, GPIO.OUT)
        GPIO.output(self.M_0, False)
        self.M_1 = 19
        GPIO.setup(self.M_1, GPIO.OUT)
        GPIO.output(self.M_1, False)
        self.M_2 = 26
        GPIO.setup(self.M_2, GPIO.OUT)
        GPIO.output(self.M_2, False)

        # Microsteps, in binary returns different modes on stepper
        if micro_steps == '0':
            print("FULL")
            GPIO.output(self.M_0, False)
            GPIO.output(self.M_1, False)
            GPIO.output(self.M_2, False)
            self.factor = 200

        elif micro_steps == '1':
            print("HALF")
            GPIO.output(self.M_0, True)
            GPIO.output(self.M_1, False)
            GPIO.output(self.M_2, False)
            self.factor = 400

        elif micro_steps == '2':
            print("1/4")
            GPIO.output(self.M_0, False)
            GPIO.output(self.M_1, True)
            GPIO.output(self.M_2, False)
            self.factor = 800

        elif micro_steps == '3':
            print("1/8")
            GPIO.output(self.M_0, True)
            GPIO.output(self.M_1, True)
            GPIO.output(self.M_2, False)
            self.factor = 1600

        elif micro_steps == '4':
            print("1/16")
            GPIO.output(self.M_0, False)
            GPIO.output(self.M_1, False)
            GPIO.output(self.M_2, True)
            self.factor = 3200

        elif micro_steps == '5':
            print("1/32")
            GPIO.output(self.M_0, True)
            GPIO.output(self.M_1, False)
            GPIO.output(self.M_2, True)
            self.factor = 6400
        else:
            print ("No micro. running full step")

        # Set all pins as output
        for pin in self.higher + self.lower + self.rot + self.claw:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)

        # Start poss on robatarm in degrees
        self.a_high = float(start_high)
        self.a_low = float(start_low)
        self.a_rot = float(start_rot)

        # Memory formula: Angle of last poss
        self.memory = {
        "high": self.a_high,
        "lower": self.a_low,
        "rot": self.a_rot
        }

        # Koordinater objekt

# Argument: Motor STRING, Steps to take, Diretions of the motor (0,1), speed (sec)
    def move(self,motor,steps,dira,speed):

        # Motor to choose/pins to choose
        if (motor.lower() == "higher"):
            pinset = self.higher
        elif (motor.lower() == "lower"):
            pinset = self.lower
        elif (motor.lower() == "rot"):
            pinset = self.rot
        else:
            print("Wrong Motor")
            pass

        # Dir pin on DRV8225.
        self.dir(dira, pinset[1])

        time.sleep(0.1)
        # Steps
        StepCounter = 0
        while StepCounter < int(steps):
            #turning the GPIO on and off tells the easy driver to take one step
            GPIO.output(pinset[0], True)
            time.sleep(speed)
            GPIO.output(pinset[0], False)
            StepCounter += 1
            time.sleep(speed)

            #Wait before taking the next step...this controls rotation speed

        # Reset pins, to false see def reset_pins
        #self.reset_pins()

    def reset_pins(self):
        for pin in self.higher + self.lower + self.rot + self.claw:
            GPIO.output(pin, False)

    def dir(self, dira, pin):
        if (dira == 0):
            GPIO.output(pin, False)
        else:
            GPIO.output(pin, True)


    def AngleToStep(self, angle):
        try:
            # Tandhjul konstant
            k = 32/9
            # et step i degrees
            c = 360/self.factor
            # Step fra angle
            step = (k*angle)/c
            #return step til brug
            return step
        except ZeroDivisionError as err:
            print("Der bliver divideret med 0:  {}".format(err))
        else:
            pass

    def inverse(self, coord):
        # Array to sort old coords
        x = coord[0]
        y = coord[1]
        z = coord[2]

        # Math to kinematics
        rrot = math.sqrt(x**2+y**2)
        rside = math.sqrt(rrot**2+z**2)
        rota = math.asin(x/rrot)
        high = 2*math.acos(rside/24)
        omega = math.asin(rrot/rside)
        a = (math.pi - high) / 2
        phi = a - (math.pi / 2)
        if z >= 0:
            low = omega + phi
        else:
            low = (math.pi - omega) + phi
        highmm = high + low


        # Subtrakt gamle dregrees
        highm = math.degrees(highmm) - (self.memory["high"])
        lower = math.degrees(low) - (self.memory["lower"])
        rot = math.degrees(rota) - (self.memory["rot"])

        # Debug
        print ("degrees - highm: {} lower: {} rot: {}".format(round(highm),round(lower),round(rot)))

        # save degrees
        self.memory["high"] = math.degrees(highmm)
        self.memory["lower"] = math.degrees(low)
        self.memory["rot"] = math.degrees(rota)
        print("{}, {}, {}".format(self.memory["high"],self.memory["lower"],self.memory["rot"]))

        # Rounding data and convert to steps
        data = [
        self.AngleToStep(round(highm)),
        self.AngleToStep(round(lower)),
        self.AngleToStep(round(rot))
        ]
        return data

    def main(self, coord):
        print(coord)
        # Calc inverse kinematics
        print("Calculation of Inverse Kinematics")

        # Store
        data = self.inverse(coord)

        # Variable to change motor speed
        speed = 0.0005

        # Debug
        print("Moving motors, high: {} lower: {} rot: {}".format(round(data[0]),round(data[1]),round(data[2])))

        # Higher motor
        if data[0] > 0:
            d_higher = 1
        else:
            d_higher = 0

        #lower
        if data[1] > 0:
            d_lower = 0
        else:
            d_lower = 1

        #rot
        if data[2] > 0:
            d_rot = 0
            print(d_rot)
        else:
            d_rot = 1
            print(d_rot)

        time.sleep(0.001)
        # Threading to move motors
        higher = Thread(target=self.move, args=("higher",math.fabs(data[0]),d_higher,speed))
        lower = Thread(target=self.move, args=("lower",math.fabs(data[1]),d_lower,speed))
        rot = Thread(target=self.move, args=("rot",math.fabs(data[2]),d_rot,speed))

        #Start Threading
        higher.start()
        time.sleep(speed*10)
        lower.start()
        rot.start()

        # Wait for threading to be done
        while higher.is_alive() == True or \
              lower.is_alive() == True or \
              rot.is_alive() == True:
            time.sleep(0.001)

        # Sleep to insure pos
        time.sleep(0.001)

        #debug
        print("Threading complete")
