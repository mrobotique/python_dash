import os

sudoPassword = 'raspberry'
command = 'arp-scan -l'


ouput = os.popen( "echo %s | sudo -S %s" % (sudoPassword,command) ).read()

if('5c:51:88:8c:a2:02' in ouput):
    print "yes"
else :
    print "no"



