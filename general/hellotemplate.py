#!/usr/bin/python
#------------------------------------------------
# Script name: hellotemplate.py
#
# Description: 
# This script is a generic command line Python app template.
# The example shows how to nicely handle parameter requirements 
# and parsing parameters. 
#
# Pip packages needed:
# arparse built-in.
#
# IBM i header if used there
# !/QOpenSys/pkgs/bin/python3
#
# Parameters
# --parm1=Parm 1
# --parm2=Parm 2
# --parm3=Parm 3
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
import argparse
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
appdesc="This is the app desc"
exitcode=0 #Init exitcode
exitmessage='' #Init the exit message
parmsexpected=3; #How many parms do we need ?

 
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
   #if len(sys.argv) < parmsexpected + 1:
   #     raise Exception(str(parmsexpected) + ' required parms - [Parm 1] [Parm 2] [Parm 3]. Process cancelled.')
   
   # Set up the command line argument parsing
   # If the parse_args function fails, the program will
   # exit with an error 2. In Python 3.9, there is 
   # an argument to prevent an auto-exit
   parser = argparse.ArgumentParser()
   parser.add_argument('-o', '--output', action='store_true', 
          help="shows output")
   parser.add_argument('--parm1', required=True,help="This is parm 1")
   parser.add_argument('--parm2', required=True,help="This is parm 2")
   parser.add_argument('--parm3', default="True",required=False,help="This is optional parm 3. Default value=True")
   # Parse the command line arguments 
   args = parser.parse_args()
   
   # Set parameter work variables from command line args
   parmscriptname = sys.argv[0]    #Script name
   parm1 = args.parm1              #Parameter 1
   parm2 = args.parm2              #Parameter 2
   parm3 = str2bool(args.parm3)    #Parameter 3 - boolean
   
   # Output parameter variables to log file
   print("Parameters:")
   print("Parm 1: " + parm1)
   print("Parm 2: " + str(parm2))
   print("Parm 3: " + str(parm3))

   # Do some work now 
   print("Hello World.")
   
   # Set success info
   exitcode=0
   exitmessage=appdesc +" completed normally."

#------------------------------------------------
# Handle Exceptions
#------------------------------------------------
# System Exit occurred. Most likely from argument parser
except SystemExit as ex:
     print("Command line argument error.")
     exitcode=ex.code # set return code for stdout
     exitmessage=str(ex) # set exit message for stdout
     #print('Traceback Info') # output traceback info for stdout
     #traceback.print_exc()
     sys.exit(99)           

except argparse.ArgumentError as exc:
     exitcode=99 # set return code for stdout
     exitmessage=str(exc) # set exit message for stdout
     #print('Traceback Info') # output traceback info for stdout
     #traceback.print_exc()      
     sys.exit(99)

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
