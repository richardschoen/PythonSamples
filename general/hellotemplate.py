#!/QOpenSys/pkgs/bin/python3
#------------------------------------------------
# Script name: hellotemplate.py
#
# Description: 
# This script is a generic command line Python app template
#
# Pip packages needed:
# pip3 install xxxxx
#
# Parameters
# P1=Parm 1
# P2=Parm 2
#------------------------------------------------
# Useful Python links (any links that are educational for this script)
# https://stackoverflow.com/questions/53864260/no-hostkey-for-host-found-when-connecting-to-sftp-server-with-pysftp-usi
# https://pysftp.readthedocs.io/en/release_0.2.8/pysftp.html
#------------------------------------------------
# Imports
#------------------------------------------------
import sys
from sys import platform
import os
import time
import traceback
import ibm_db_dbi as db2 
import xlrd
import csv
import datetime as dt
from string import Template 
from urllib.parse import unquote

#------------------------------------------------
# Script initialization
#------------------------------------------------

# Initialize or set variables
appdesc="This is the app desc"
exitcode=0 #Init exitcode
exitmessage='' #Init the exit message
parmsexpected=3; #How many parms do we need ?

#Output messages to STDOUT for logging
print("-------------------------------------------------------------------------------")
print(appdesc)
print("Start of Main Processing - " + time.strftime("%H:%M:%S"))
print("OS:" + platform)

#------------------------------------------------
# Main script logic
#------------------------------------------------
try: # Try to perform main logic
   
   # Check to see if all required parms were passed
   if len(sys.argv) < parmsexpected + 1:
        raise Exception(str(parmsexpected) + ' required parms - [Parm 1] [Parm 2] [Parm 3]. Process cancelled.')
   
   # Set parameter work variables from command line args
   parmscriptname = sys.argv[0]    #Script name
   parm1 = sys.argv[1]             #Parameter 1
   parm2 = int(sys.argv[2])        #Parameter 2 - integer
   parm3 = eval(sys.argv[3])       #Parameter 3 - boolean

   # Output parameter variables to log file
   print("Parameters:")
   print("Parm 1: " + parm1)
   print("Parm 2: " + str(parm2))
   print("Parm 3: " + str(parm3))

   print("Hello World")
   
   # Set success info
   exitcode=0
   exitmessage=appdesc +" completed normally."

#------------------------------------------------
# Handle Exceptions
#------------------------------------------------
except Exception as ex: # Catch and handle exceptions
   exitcode=99 # set return code for stdout
   exitmessage=str(ex) # set exit message for stdout
   print('Traceback Info') # output traceback info for stdout
   traceback.print_exc()        

#------------------------------------------------
# Always perform final processing. Output exit message and exit code
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
