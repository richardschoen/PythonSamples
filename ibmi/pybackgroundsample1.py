#!/QOpenSys/pkgs/bin/python3
#------------------------------------------------
# Script name: pybackgroundsample1.py
#
# Description: 
# This is a sample background process script that loops every xx seconds to do some work.
# After performing work, the script goes back to sleep so it doesn't churn the system CPU.  
#
# Parameters:
# --processidfile - File to receive the process ID for when we need 
#   to shut down process immediately. 
#   Default: /tmp/pybackgroundsample1.pid
#
# --waitinterval - How many seconds to wait after each polling/processing cycle. 
#   Default: 10 (10 seconds)
#
# --forcerestart - Force restart even if process ID file already exists ? (True/False)
#                  This help prevent multiple versions of the same process from running
#                  at the same time.
#   Default: False (False=Do not force restart) 
#
# Pip packages needed:
# None - argparse is a standard module.
#
# Returns:
# Exits with 0 on success or 99 on errors.
# This allows us to communicate back to command line with an appropriate return code.
#
#------------------------------------------------
# Web Links
# https://polling2.readthedocs.io/en/latest/ - An alternative polling engine to look at.
# https://stackoverflow.com/questions/20170251/how-to-run-a-script-forever
#------------------------------------------------

import requests
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
exitcode=0 #Init exitcode
exitmessage=''
processcancelled=False

#Output messages to STDOUT for logging
print("-------------------------------------------------------------------------------")
print("Script: " + sys.argv[0])
print("Start of Main Processing - " + time.strftime("%H:%M:%S"))
print("OS:" + platform)

 
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

def do_work():
    #-------------------------------------------------------
    # Function: do_work
    # Desc: This function is where work should happen
    # :return: 
    #-------------------------------------------------------    
    print("Hello, World background " + str(time.strftime("%H:%M:%S")))


#------------------------------------------------
# Main script logic
#------------------------------------------------
try: # Try to perform main logic      

   # Set up the command line argument parsing
   # If the parse_args function fails, the program will
   # exit with an error 2. In Python 3.9, there is 
   # an argument to prevent an auto-exit
   parser = argparse.ArgumentParser()
   parser.add_argument('--processidfile', required=False,default='/tmp/pybackgroundsample1.pid',help="Process id output file")
   parser.add_argument('--waitinterval', required=False,default=10,help="Polling wait interval. 10 seconds default.")
   parser.add_argument('--forcerestart', required=False,default='False',help="Force restart if process ID file exists. default=False.")
   
   # Parse the command line arguments 
   args = parser.parse_args()
      
   # Set parameter work variables from command line args
   parmscriptname = sys.argv[0] 
   parmoutputfile = args.processidfile      
   parmwaitinterval= int(args.waitinterval)
   parmforcerestart = str2bool(args.forcerestart)
   print(f"Python script: {parmscriptname}")
   print(f"Output process ID file: {parmoutputfile}")
   print(f"Wait interval: {parmwaitinterval}")
   print(f"Force restart: {parmforcerestart}")

   # Check for existing process id file and bail if found
   exists1 = os.path.isfile(parmoutputfile)
   # If exists now, the process may already be running
   if exists1:
       # If force restart, kill process ID file and continue 
       if parmforcerestart:
          print(f"Removing existing process ID file {parmoutputfile} before starting process.") 
          os.remove(parmoutputfile)
       # Bail out if process ID file exists and Force restart = False    
       else:    
          raise Exception('Process ID file ' + parmoutputfile + ' exists. Process may already be running. Process cancelled.')

   # Write new process id file with curent process ID. 
   # If process ID file gets destroyed, then we can end our process work
   # on next polling interval.
   # Open the process id file and write it.  
   f = open(parmoutputfile,"a+")
   f.write(str(os.getpid())) 
   f.close()

   # Display the process ID in stdout
   print('process id:' + str(os.getpid())  )

   # Infinite while loop until process is cancelled
   while True and processcancelled==False:
   
      # Do the work for each cycle.
      # Put all work in do_work or run it inline. Your choice.
      do_work()

      # Wait for next cycle
      time.sleep(parmwaitinterval) #make function to sleep for 10 seconds
      
      # Check for existing process id file and end process if not found
      # This means someone has triggered the process end by deleting process ID file.
      exists = os.path.isfile(parmoutputfile)
      if exists==False:
         processcancelled=True # Set cancelled flag
         print('Process ID file ' + parmoutputfile + ' does not exist any more. Process cancelled.')
         ## Skip raising exception and nicely exit instead.
         ##raise Exception('Process ID file ' + parmoutputfile + ' does not exist any more. Process cancelled.')
   
   # Set success info
   exitcode=0
   exitmessage='Completed successfully'

#------------------------------------------------
# Handle Exceptions
#------------------------------------------------
# System Exit occurred. Most likely from argument parser
except SystemExit as ex:
     print("Command line argument error.")
     exitcode=ex.code # set return code for stdout
     exitmessage=str(ex) # set exit message for stdout
     print('Traceback Info') # output traceback info for stdout
     traceback.print_exc()      

except argparse.ArgumentError as exc:
     exitcode=99 # set return code for stdout
     exitmessage=str(exc) # set exit message for stdout
     print('Traceback Info') # output traceback info for stdout
     traceback.print_exc()      
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
