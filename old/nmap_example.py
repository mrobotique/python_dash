import nmap
nm = nmap.PortScanner()
data = nm.scan(hosts='192.168.0.1/24',arguments='-O')
print data['nmap']['scanstats']['uphosts']
