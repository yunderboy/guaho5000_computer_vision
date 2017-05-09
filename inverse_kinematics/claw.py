import RPi.GPIO as GPIO
import time

class Claw(object):
    def __init__(self):
        # Board mode
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # set control pins
        self.coil_A_1_pin = 18
        self.coil_A_2_pin = 24
        self.coil_B_1_pin = 23
        self.coil_B_2_pin = 25
        self.time = 0.005

        # GPIO setup for pins
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)

        # reset pins to reduce watt
        self.resetPins()

    def forward(self,steps):
        # delay for speed
        delay = self.time

        # For loop for running stepper cycle
        for i in range(0, steps):
            self.setStep(1, 0, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(delay)
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)

        # reset pins to reduce watt
        time.sleep(0.001)
        self.resetPins()

    def backwards(self,steps):
        # Delay for speed
        delay = self.time

        # For loop for running stepper cycle
        for i in range(0, steps):
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(1, 0, 1, 0)
            time.sleep(delay)

        # reset pins to reduce watt
        time.sleep(0.001)
        self.resetPins()

    def setStep(self, w1, w2, w3, w4):
        # Function for writing GPIO stepper cycle
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)

    def resetPins(self):
        GPIO.output(self.coil_A_1_pin, 0)
        GPIO.output(self.coil_A_2_pin, 0)
        GPIO.output(self.coil_B_1_pin, 0)
        GPIO.output(self.coil_B_2_pin, 0)
