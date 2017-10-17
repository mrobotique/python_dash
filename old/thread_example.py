from threading import Thread
from Queue import Queue
import time
import RPi.GPIO as GPIO
import time
import os

sudoPassword = 'raspberry'
command = 'arp-scan -l'
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor

global ouput

def thread1():
    #read variable "a" modify by thread 2
    global ouput
    while True:
##        a = q.get()
        i=GPIO.input(11)
        if(i):
            if ('5c:51:88:8c:a2:02' in ouput):
                print "No problem"
            else:
                print "Intruder"
        print i
        time.sleep(0.2)

def thread2(): ##PIR
    global ouput
    while(True):
        ouput = os.popen( "echo %s | sudo -S %s" % (sudoPassword,command) ).read()
        
        #q.put(ouput)

        
    
ouput = ""
queue = Queue()
thread1 = Thread( target=thread1)
thread2 = Thread( target=thread2)

thread1.start()
thread2.start()
thread1.join()
thread2.join()

