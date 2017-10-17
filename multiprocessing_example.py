import multiprocessing
import time
import RPi.GPIO as GPIO
import time
import os
from Queue import Queue, Empty

sudoPassword = 'raspberry'
command = 'arp-scan -l'
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor

global ouput
global continueA

def thread1():
    global continueA
    #read variable "a" modify by thread 2
    global ouput
    while continueA:
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
    global continueA
    
    while(continueA):
        ouput = os.popen( "echo %s | sudo -S %s" % (sudoPassword,command) ).read()
        
        #q.put(ouput)

        
    


def main():
    global ouput
    global continueA
    continueA = True
    service = multiprocessing.Process(name='thread2', target=thread2)
    Pir= multiprocessing.Process(target=thread1) # use default name
    
    service.start()
    Pir.start()

    

    time.sleep(5)
    print "hola"
    service.finished = True
    Pir.finished = True

    service.join()
    Pir.join()
    


    
if __name__ == "__main__":
    try:
        main()
    except:
        print 'kaput'
