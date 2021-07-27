#!/usr/bin/python
#------------------------------------------------
# Script name: pyodbcconnectiontest.py
#
# Description: 
# Open and Close ODBC Connection to test ODBC connectivity.
# Once you set the correct connection string, you can just 
# run this script to open and close your ODBC connection to 
# make sure the ODBC driver works as expected. 
#
# Pip packages needed:
# pip3 install pyodbc
#
# ODBC requirements: 
# If running from PC: 
# Install IBM ACS ODBC Driver, Python3.x and PYODBC - via pip3 
# If running from IBMi: 
# Install IBM ACS ODBC Driver, Python3.x and PYODBC - via pip3 
#
# Parameters
# None
#------------------------------------------------
# Imports
#------------------------------------------------
import sys
from sys import platform
import time
import traceback
import datetime as dt
import pyodbc as db2

#------------------------------------------------
# Script initialization
#------------------------------------------------

# Initialize or set variables
exitcode=0 #Init exitcode
exitmessage=''
parmsexpected=0;

#Output messages to STDOUT for logging
print("-------------------------------------------------------------------------------")
print("IBM ODBC Connection Test Sample")
print("Start of Main Processing - " + time.strftime("%H:%M:%S"))

#------------------------------------------------
# Main script logic
#------------------------------------------------
try: # Try to perform main logic

   # TODO - Uncomment whichever connection string sample you want to use  

   # ODBC default *LOCAL DSN connection string when running natively in PASE
   # *LOCAL DSN gets created when PASE ODBC driver is installed. 
   # (Assumes script running from PASE/SSH)
   connstring = 'DSN=*LOCAL;CommitMode=0;'
   
   # ODBC connection string for localhost IBM i system with login credentials
   # Need to set your IBM i system name, user and password 
   # (Assumes script running from PASE/SSH)
   #connstring = 'Driver={IBM i Access ODBC Driver};System=localhost;Uid=IBMIUSER;Pwd=IBMIPASS;CommitMode=0;'
   
   # ODBC connection string for named IP address or host name with login credentials 
   # Need to set your IBM i system name, user and password 
   # (Universal connection string for PC, Linux or IBMi)
   #connstring = 'Driver={IBM i Access ODBC Driver};System=192.168.1.1;Uid=IBMIUSER;Pwd=IBMIPASS;CommitMode=0;'

   # Connect to database
   conn = db2.connect(connstring)
   
   # Was connect successful ?
   if conn != None:
      print("ODBC connection was successful")
   else:
      raise Exception('ODBC connection failed') 

   # Close database connection
   conn.close() 
   
   # Set success info
   exitcode=0
   exitmessage="ODBC connection test completed successfully."

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
