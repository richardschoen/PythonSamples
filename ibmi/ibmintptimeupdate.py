#!/QOpenSys/pkgs/bin/python3
#------------------------------------------------
# Script name: ibmintptimeupdate.py
#
# Description: 
# This script will get the current time from a remote
# NTP server and update IBM i system time using the 
# CHGSYSVAL command with system value QTIME.
#
# Parameters
# None
#------------------------------------------------

import sys
from sys import platform
import os
import re
import time
import traceback
import socket
import struct

#------------------------------------------------
# Script initialization
#------------------------------------------------

# Initialize or set variables
exitcode=0 # Init exitcode
exitmessage='' # Exit message
ntpserver="0.north-america.pool.ntp.org" # Time server to use

#------------------------------------------------
# Declare functions
#------------------------------------------------
def RequestTimefromNtp(addr='0.north-america.pool.ntp.org'):
    REF_TIME_1970 = 2208988800  # Reference time
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    client.sendto(data, (addr, 123))
    data, address = client.recvfrom(1024)
    if data:
        t = struct.unpack('!12I', data)[10]
        t -= REF_TIME_1970
        return time.ctime(t), t
    
def RequestTimefromNtp2(addr='0.north-america.pool.ntp.org'):
    REF_TIME_1970 = 2208988800  # Reference time
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    client.sendto(data, (addr, 123))
    data, address = client.recvfrom(1024)
    if data:
        t = struct.unpack('!12I', data)[10]
        t -= REF_TIME_1970
        #return time.strftime("%d %m %Y, %H:%M", time.localtime(t))
        #return time.ctime(t)
        return time.strftime("%H%M%S", time.localtime(t))

# Output messages to STDOUT for logging
print("-------------------------------------------------------------------------------")
print(f"Updating System Time from NTP Server: {ntpserver}")
print("Start of Main Processing - " + time.strftime("%H:%M:%S"))
print("OS:" + platform)

#------------------------------------------------
# Main script logic
#------------------------------------------------
try: # Try to perform main logic

  if __name__ == "__main__":

        print(f"Current time from NTP server:{RequestTimefromNtp()}")
        newtime=(RequestTimefromNtp2(ntpserver))
         
        # Display system value for QTIME before change 
        print("Display QTIME before update")
        cmd = f"system \"DSPSYSVAL SYSVAL(QTIME)\""
        print(cmd) 
        returned_value = os.system(cmd)  # returns the exit code in unix
        print('returned value:', returned_value)
        
        # Update QTIME value now 
        print("Update QTIME value")
        cmd = f"system \"CHGSYSVAL SYSVAL(QTIME) VALUE('{newtime}')\""
        print(cmd) 
        returned_value = os.system(cmd)  # returns the exit code in unix
        print('returned value:', returned_value)
        
        # Display system value for QTIME before change 
        print("Display QTIME after update")
        cmd = f"system \"DSPSYSVAL SYSVAL(QTIME)\""
        print(cmd) 
        returned_value = os.system(cmd)  # returns the exit code in unix
        print('returned value:', returned_value)
    
  
        # Set success info
        exitcode=0
        exitmessage=f"NTP time update completed successfully."
 
#------------------------------------------------
# Handle Exceptions
#------------------------------------------------
except Exception as ex: # Catch and handle exceptions
   exitcode=99 # set return code for stdout
   exitmessage=str(ex) # set exit message for stdout
   print('Traceback Info') # output traceback info for stdout
   traceback.print_exc()        

#------------------------------------------------
# Always perform final processing
#------------------------------------------------
finally: # Final processing
    # Do any final code and exit now
    # We log as much relevent info to STDOUT as needed
    print('ExitCode:' + str(exitcode))
    print('ExitMessage:' + exitmessage)
    print("End of Main Processing - " + time.strftime("%H:%M:%S"))
    print("-------------------------------------------------------------------------------")
    
    # Exit the script now
    sys.exit(exitcode) 
  
    
    
