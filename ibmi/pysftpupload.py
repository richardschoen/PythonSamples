#!/QOpenSys/pkgs/bin/python3
#------------------------------------------------
# Script name: pysftpupload.py
#
# Description: 
# This script will upload a specified local file to a remote sftp server.
#
# TODO Items:  
# This version utilizes user ID and password, not a private key.
#
# Pip packages needed:
# pip3 install pysftp
#
# Parameters
# P1=SFTP Host
# P2=SFTP Port
# p3=SFTP User
# p4=SFTP Password
# P5=From local file
# p6=To remote file
# p7=Replace remote file it it exists. (True/False)
#------------------------------------------------
# Useful Python links
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
import pysftp

#------------------------------------------------
# Script initialization
#------------------------------------------------

# Initialize or set variables
appname="Uploading File via SFTP"
exitcode=0 #Init exitcode
exitmessage='' #Init the exit message
parmsexpected=7; #How many parms do we need ?

#Output messages to STDOUT for logging
print("-------------------------------------------------------------------------------")
print(appname)
print("Start of Main Processing - " + time.strftime("%H:%M:%S"))
print("OS:" + platform)

#------------------------------------------------
# Main script logic
#------------------------------------------------
try: # Try to perform main logic
   
   # Check to see if all required parms were passed
   if len(sys.argv) < parmsexpected + 1:
        raise Exception(str(parmsexpected) + ' required parms - [SFTP Host] [SFTP Port] [SFTP User] [SFTP Pass] [Local File to Upload] [Remote Destination File] [Replace-True/False]. Process cancelled.')
   
   # Set parameter work variables from command line args
   parmscriptname = sys.argv[0]    #Script name
   parmsftphost = sys.argv[1]      #SFTP host name/ip
   parmsftpport = int(sys.argv[2]) #Convert port to integer
   parmsftpuser= sys.argv[3]       #SFTP User  
   parmsftppass= sys.argv[4]       #SFTP Password
   parmfromlocalfile= sys.argv[5]  #From local file
   parmsftptofile= sys.argv[6]     #To remote Ftp file
   parmreplace= eval(sys.argv[7])  #Replace local file if it exists-(True/False)

   # Output parameter variables to log file
   print("Parameters:")
   print("SFTP Host: " + parmsftphost)
   print("SFTP Port: " + str(parmsftpport))   
   print("SFTP User: " + parmsftpuser)
   print("From Local File: " + parmfromlocalfile)
   print("To Remote File: " + parmsftptofile)   
   print("Replace file: " + str(parmreplace))
   
   # Sample SFTP options
   cnopts = pysftp.CnOpts()
   cnopts.hostkeys = None

   # Connect via User and Password   
   with pysftp.Connection(parmsftphost, port=parmsftpport, username=parmsftpuser, password=parmsftppass,private_key=None,private_key_pass=None,cnopts=cnopts) as sftp:

      ###with sftp.cd('/tmp'):           #Ex: temporarily chdir to selected dir if needed

      # Make sure local file exists
      # Old 1/13/2022 - if sftp.isfile(parmfromlocalfile)==False:
      if os.path.isfile(parmfromlocalfile)==False:
         raise Exception("Local file " + parmfromlocalfile + " doesn't exist. Process cancelled.")
  
      # Make sure remote output file does not exist
      if sftp.isfile(parmsftptofile):
         if parmreplace: # If replace, delete existing file
            sftp.remove(parmsftptofile)
         else: # Bail out if found and replace not selected
            raise Exception('Remote file ' + parmsftptofile + ' exists and replace not selected. Process cancelled.')          
        
      print("Uploading file " + parmfromlocalfile + " to " + parmsftptofile)
      # sftp.put('/pycode/filename')  	# upload file to allcode/pycode on remote
      sftp.put(parmfromlocalfile,parmsftptofile) # put local file to remote file   

   # Set success info
   exitcode=0
   exitmessage=appname + " was successful."

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
