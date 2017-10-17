#!/usr/bin/python
"""
Created on Tue Oct 17 16:32:14 2017
@author: mromero
"""
import RPi.GPIO as GPIO
import time

PIR_Input_pin = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_Input_pin, GPIO.IN)         #Read output from PIR motion sensor

def main(pin,delay):
	i=GPIO.input(pin)
	time.sleep(delay)
	return i
	
if __name__ == "__main__":
    try:
		while(True):
			print main(PIR_Input_pin,0.2)
    except:
		print "error"
		
