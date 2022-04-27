import re
import sys
import time
import subprocess
import telnetlib

user = "nms_user"
password = "nms_pwd"
    
def get_utility():
    cmd = "display interface brief | include %s\n" % interface
    regex = interface + "[^.].+\s(\d{1,}?\.\d{2})%.*?\s(\d{1,}?\.\d{2})%.+\r$"
    tn = telnetlib.Telnet()
    tn.open(hostname, timeout=5)
    time.sleep(0.5)
    tn.write(user + "\n")
    tn.write(password + "\n")
    tn.read_until(">")
    tn.write(cmd)
    tn.write(chr(26))
    tn.write("quit\n")
    raw = tn.read_until(">")
    res = re.search(regex, raw, re.MULTILINE)
    if res:
        print "input:%s output:%s" % (res.group(1) , res.group(2))
    else:
        print "input:0 output:0"
    tn.close()
    
    

if __name__ == '__main__':
    if (len(sys.argv) > 1):
	hostname = sys.argv[1]
	interface = sys.argv[2]
        get_utility()
    else:
	print "input:0 output:0"
