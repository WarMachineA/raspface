import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

SERVO = 25

GPIO.setup(SERVO, GPIO.OUT)

PWM = GPIO.PWM(SERVO, 50)

GPIO.setwarnings(False)

PWM.start(0)

def SetAngle(angle):
    duty = angle/18+2
    GPIO.output(SERVO,True)
    PWM.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(SERVO,False)
    PWM.ChangeDutyCycle(0)
SetAngle(90)