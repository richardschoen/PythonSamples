#!/usr/bin/python
#------------------------------------------------
# Script name: hello_args_sample1.py
#
# Description: 
# This script is a generic command line Python app template.
# The example shows how to handle parameter requirements 
# and parsing parameters. 
#
# Pip packages needed:
# None
#
# IBM i header if used there
# !/QOpenSys/pkgs/bin/python3
#
# Parameters in ordinal order on command line
# parm1=Parm 1
# parm2=Parm 2
# parm3=Parm 3
#------------------------------------------------
# Useful Python links (any links that are educational for this script)
# http://zetcode.com/python/argparse/
# https://stackoverflow.com/questions/5943249/python-argparse-and-controlling-overriding-the-exit-status-code
# https://www.techbeamers.com/use-try-except-python/
# argument parse exceptions
# https://stackoverflow.com/questions/8107713/using-argparse-argumenterror-in-python
#------------------------------------------------
# Imports
#------------------------------------------------
import sys
from sys import platform
import os
import re
import time
import traceback 

#------------------------------------------------
# Script initialization
#------------------------------------------------

# Initialize or set variables
appdesc="This is hello_args_sample1"
exitcode=0 #Init exitcode
exitmessage='' #Init the exit message
parmsexpected=3; #How many parms do we need ?

#------------------------------------------------
# Define internal functions
#------------------------------------------------
 
def str2bool(strval):
    #-------------------------------------------------------
    # Function: str2bool
    # Desc: Constructor
    # :strval: String value for true or false
    # :return: Return True if string value is" yes, true, t or 1
    #-------------------------------------------------------
    return strval.lower() in ("yes", "true", "t", "1")

def trim(strval):
    #-------------------------------------------------------
    # Function: trim
    # Desc: Alternate name for strip
    # :strval: String value to trim. 
    # :return: Trimmed value
    #-------------------------------------------------------
    return strval.strip()

def rtrim(strval):
    #-------------------------------------------------------
    # Function: rtrim
    # Desc: Alternate name for rstrip
    # :strval: String value to trim. 
    # :return: Trimmed value
    #-------------------------------------------------------
    return strval.rstrip()

def ltrim(strval):
    #-------------------------------------------------------
    # Function: ltrim
    # Desc: Alternate name for lstrip
    # :strval: String value to ltrim. 
    # :return: Trimmed value
    #-------------------------------------------------------
    return strval.lstrip()

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
   # Note: Old way to check if all parms passed
   if len(sys.argv) < parmsexpected + 1:
        raise Exception(str(parmsexpected) + ' required parms - [Parm 1] [Parm 2] [Parm 3]. Process cancelled.')
   
   # Set parameter work variables from command line args
   parmscriptname = sys.argv[0]     #Script name
   parm1 = sys.argv[1]              #Parameter 1
   parm2 = sys.argv[2]              #Parameter 2
   parm3 = str2bool(sys.argv[3])    #Parameter 3 - boolean
   
   # Output parameter variables 
   print("Parameters:")
   print("Parm 1: " + parm1)
   print("Parm 2: " + str(parm2))
   print("Parm 3: " + str(parm3))

   # TODO - Do some real work now 
   print("Hello World.")
   
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
     sys.exit(99)

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
