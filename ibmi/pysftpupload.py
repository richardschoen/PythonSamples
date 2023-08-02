#!/QOpenSys/pkgs/bin/python3
#------------------------------------------------
# Script name: pysftpupload.py
#
# Description: 
# This script will upload a specified local file to a remote sftp server.
# This version utilizes user ID and password or a user and private key file.
#
# Pip packages needed:
# pip3 install pysftp
# pip3 install pysftp-extension
#
#
# Parameters
# --sftphost/-host=SFTP Host
# --sftpport/-port=SFTP Port
# --sftpuser/-user=SFTP User (User name is always required)
# --sftppass/-pass=SFTP Pass (Pasword can be empty if using private key)
# --privatekeyfile/-privatekey=SFTP SSH private key file
# --privatekeypass/-privatepass=SFTP SSH private key password if there is one
# --fromlocalfile/-fromfile=Local file to upload
# --toremotefile/-tofile=Remote file to upload to
# --replacefile/-replace=Remote remote to file if it exists. True/False Default=False
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
import datetime as dt
from string import Template 
from urllib.parse import unquote
import pysftp
#import pysftp_extension
import argparse

#------------------------------------------------
# Script initialization
#------------------------------------------------

# Initialize or set variables
appname="Uploading File via SFTP"
exitcode=0 #Init exitcode
exitmessage='' #Init the exit message

#Output messages to STDOUT for logging
print("-------------------------------------------------------------------------------")
print(appname)
print("Start of Main Processing - " + time.strftime("%H:%M:%S"))
print("OS:" + platform)

#------------------------------------------------
# Define some useful functions
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

#------------------------------------------------
# Main script logic
#------------------------------------------------
try: # Try to perform main logic
   
   # Set parameter work variables from command line args
   parmscriptname = sys.argv[0]    #Script name

   # Set up the command line argument parsing.
   # If the parse_args function fails, the program will
   # exit with an error 2. In Python 3.9, there is 
   # an argument to prevent an auto-exit
   # Each argument has a long and short version
   parser = argparse.ArgumentParser()
   parser.add_argument('-host','--sftphost', required=True,help="SFTP server host/ip")
   parser.add_argument('-port','--sftpport', required=True,help="SFTP port")
   parser.add_argument('-user','--sftpuser', required=True,help="SFTP user")
   parser.add_argument('-pass','--sftppass', required=True,help="SFTP password")
   parser.add_argument('-privatekey','--privatekeyfile', required=True,help="Private key file")
   parser.add_argument('-privatepass','--privatekeypass', required=True,help="Private key password")
   parser.add_argument('-fromfile','--fromlocalfile', required=True,help="Local file to upload")
   parser.add_argument('-tofile','--toremotefile', required=True,help="Remote file to upload to")
   parser.add_argument('-replace','--replacefile', default="False",required=False,help="Replace remote output file. Default value=False")
   
   # Parse the command line arguments 
   args = parser.parse_args()

   # Pull arguments into variables so they are meaningful
   parmsftphost=args.sftphost.strip()
   parmsftpport=int(args.sftpport.strip())
   parmsftpuser=args.sftpuser.strip()
   parmsftppass=args.sftppass.strip()
   parmsprivatekeyfile=args.privatekeyfile.strip()
   parmsprivatekeypass=args.privatekeypass.strip()
   parmfromlocalfile=args.fromlocalfile.strip()
   parmsftptofile=args.toremotefile.strip()
   parmreplace=str2bool(args.replacefile) 

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
   sftp=None

   # Connect via User and password or User and Private Key if key file specified  
   # https://pypi.org/project/pysftp-extension/
   if (parmsprivatekeyfile!=""): 
      sftp=pysftp.Connection(parmsftphost, port=parmsftpport, username=parmsftpuser, private_key=parmsprivatekeyfile, private_key_pass=parmsprivatekeypass, cnopts=cnopts)
   else:
      sftp=pysftp.Connection(parmsftphost, port=parmsftpport, username=parmsftpuser, password=parmsftppass,private_key=None,private_key_pass=None,cnopts=cnopts)

   # Make sure local file exists
   if os.path.isfile(parmfromlocalfile)==False:
      raise Exception("Local file " + parmfromlocalfile + " doesn't exist. Process cancelled.")
  
   # Make sure remote output file does not exist
   if sftp.isfile(parmsftptofile):
      if parmreplace: # If replace, delete existing file
         sftp.remove(parmsftptofile)
      else: # Bail out if found and replace not selected
         raise Exception('Remote file ' + parmsftptofile + ' exists and replace not selected. Process cancelled.')          
       
   print("Uploading file " + parmfromlocalfile + " to " + parmsftptofile)
   sftp.put(parmfromlocalfile,parmsftptofile) # put local file to remote file   

   # Close connection 
   sftp.close()

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
