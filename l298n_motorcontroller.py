import RPi.GPIO as GPIO 

class L298N():
    def __init__(self):
        print("[INFO] initializing L298N chip...")
        
        self.m2en, self.m2a, self.m2b = 17, 22, 27 #left motor (en, neg, pos)
        self.m1en, self.m1a, self.m1b = 25, 23, 24 #right motor (en, neg, pos)
        
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(self.m1en, GPIO.OUT)
        GPIO.setup(self.m1a, GPIO.OUT)
        GPIO.setup(self.m1b, GPIO.OUT)

        GPIO.setup(self.m2en, GPIO.OUT)
        GPIO.setup(self.m2a, GPIO.OUT)
        GPIO.setup(self.m2b, GPIO.OUT)

        GPIO.output(self.m1a, GPIO.LOW)
        GPIO.output(self.m1b, GPIO.LOW)
        self.m1pwm = GPIO.PWM(self.m1en, 100)
        self.m1pwm.start(0)

        GPIO.output(self.m2a, GPIO.LOW)
        GPIO.output(self.m2b, GPIO.LOW)
        self.m2pwm = GPIO.PWM(self.m2en, 100)
        self.m2pwm.start(0)
        
    def _set_direction(self, left_speed, right_speed):
        if left_speed > 0:
            GPIO.output(self.m2a, GPIO.HIGH)
            GPIO.output(self.m2b, GPIO.LOW)
        elif left_speed < 0:
            GPIO.output(self.m2a, GPIO.LOW)
            GPIO.output(self.m2b, GPIO.HIGH)
        else:
            GPIO.output(self.m2a, GPIO.LOW)
            GPIO.output(self.m2b, GPIO.LOW)
            
        if right_speed > 0:
            GPIO.output(self.m1a, GPIO.HIGH)
            GPIO.output(self.m1b, GPIO.LOW)
        elif right_speed < 0:
            GPIO.output(self.m1a, GPIO.LOW)
            GPIO.output(self.m1b, GPIO.HIGH)
        else:
            GPIO.output(self.m1a, GPIO.LOW)
            GPIO.output(self.m1b, GPIO.LOW)
            
        if (left_speed>0 and right_speed<0) or \
            (left_speed<0 and right_speed>0):
                left_speed = left_speed * 0.5
                right_speed = right_speed * 0.5
            
        self.m2pwm.start(abs(left_speed))
        self.m1pwm.start(abs(right_speed))
        
    def _destroy(self):
        GPIO.output(self.m1a, GPIO.LOW)
        GPIO.output(self.m1b, GPIO.LOW)

        GPIO.output(self.m2a, GPIO.LOW)
        GPIO.output(self.m2b, GPIO.LOW)

        self.m1pwm.start(0)
        self.m2pwm.start(0)

        GPIO.cleanup()         