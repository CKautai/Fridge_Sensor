#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
from urllib.request import urlopen
from gpiozero import Buzzer

LIGHT_PIN = 18   # photoresistor pin
LED_PIN = 27     #LED pin
BUZZER = Buzzer(17) #Buzzer Pin
EVENT = 'fridge_door_open'
BASE_URL = 'https://maker.ifttt.com/trigger/'
KEY = '3g853LUa9HVU4XVJHkH60CFHrPyYiUIfiLJc1Ih92n'

# Configure the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

def send_event():
    response = urlopen(BASE_URL + EVENT + '/with/key/' + KEY)
    print(response.read())
GPIO.output(LED_PIN, False)
try:
    while True:
        if GPIO.input(LIGHT_PIN) == 0:
            # Its light (door open)
            print("Fridge Open")
            GPIO.output(LED_PIN, True)
            print("Waiting one minute")
            time.sleep(60)
            if GPIO.input(LIGHT_PIN) == 0:
                send_event()
            # Beep every 30 seconds until the door is closed again
            while GPIO.input(LIGHT_PIN) == 0:
                BUZZER.on()
                time.sleep(1)
                BUZZER.off()
                time.sleep(30)
            print("Fridge Closed")
            print("Monitoring again")
            GPIO.output(LED_PIN, False)
            

finally:
    print('Cleaning up GPIO')
    GPIO.cleanup()
