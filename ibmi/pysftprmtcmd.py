#!/QOpenSys/pkgs/bin/python3
#------------------------------------------------
# Script name: pysftprmtcmd.py
#
# Description: 
# This script will run up to 5 individual remote QSH/PASE or other SSH commands over SFTP SSH channel.
# The commands are run separately.
# If you want commands run together, create a .bat file, PowerShell script or shell script to run on the remote system.
# This version utilizes user ID and password or a user and private key file.
#
# Pip packages needed:
# pip3 install pysftp
# pip3 install pysftp-extension (may not be needed)
#
# Parameters
# --sftphost/-host=SFTP Host
# --sftpport/-port=SFTP Port
# --sftpuser/-user=SFTP User (User name is always required)
# --sftppass/-pass=SFTP Pass (Pasword can be empty if using private key)
# --privatekeyfile/-privatekey=SFTP SSH private key file
# --privatekeypass/-privatepass=SFTP SSH private key password if there is one
# --command/-cmd=Remote command 1
# --command2/-cmd2=Remote command 2
# --command3/-cmd3=Remote command 3
# --command4/-cmd4=Remote command 4
# --command5/-cmd5=Remote command 5
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
import csv
import datetime as dt
from string import Template 
from urllib.parse import unquote
import pysftp
import argparse

#------------------------------------------------
# Script initialization
#------------------------------------------------

# Initialize or set variables
appname="Run remote commands over SFTP connection"
exitcode=0 #Init exitcode
exitmessage='' #Init the exit message
sshrtn=0; # init SSH return code

#Output messages to STDOUT for logging
print("-------------------------------------------------------------------------------")
print(appname)
print("Start of Main Processing - " + time.strftime("%H:%M:%S"))
print("OS:" + platform)

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
   parser.add_argument('-cmd','--command', required=True,help="Command")
   parser.add_argument('-cmd2','--command2',default="", required=False,help="Command 2")
   parser.add_argument('-cmd3','--command3',default="", required=False,help="Command 3")
   parser.add_argument('-cmd4','--command4',default="", required=False,help="Command 4")
   parser.add_argument('-cmd5','--command5',default="", required=False,help="Command 5")

   # Parse the command line arguments 
   args = parser.parse_args()

   # Pull arguments into variables so they are meaningful
   parmsftphost=args.sftphost.strip()
   parmsftpport=int(args.sftpport.strip())
   parmsftpuser=args.sftpuser.strip()
   parmsftppass=args.sftppass.strip()
   parmcommand=args.command.strip()
   parmcommand2=args.command2.strip()
   parmcommand3=args.command3.strip()
   parmcommand4=args.command4.strip()
   parmcommand5=args.command5.strip()
   parmsprivatekeyfile=args.privatekeyfile.strip()
   parmsprivatekeypass=args.privatekeypass.strip()

   # Output parameter variables to log file
   print("Parameters:")
   print("SFTP Host: " + parmsftphost)
   print("SFTP Port: " + str(parmsftpport))   
   print("SFTP User: " + parmsftpuser)
   print("Command 1: " + parmcommand)
   print("Command 2: " + parmcommand2)
   print("Command 3: " + parmcommand3)
   print("Command 4: " + parmcommand4)
   print("Command 5: " + parmcommand5)
   
   # Sample SFTP options
   cnopts = pysftp.CnOpts()
   cnopts.hostkeys = None

   # Connect via User and password or User and Private Key if key file specified   
   # https://pypi.org/project/pysftp-extension/
   if (parmsprivatekeyfile!=""):
      sftp=pysftp.Connection(parmsftphost, port=parmsftpport, username=parmsftpuser, private_key=parmsprivatekeyfile, private_key_pass=parmsprivatekeypass, cnopts=cnopts)
   else:
      sftp=pysftp.Connection(parmsftphost, port=parmsftpport, username=parmsftpuser, password=parmsftppass,private_key=None,private_key_pass=None,cnopts=cnopts)
   
      ##sftp.server_extensions={'server-sig-algs','ssh-rsa'}
      ###with sftp.cd('/tmp'):           #Ex: temporarily chdir to selected dir if needed

   # Run command 1
   if parmcommand.strip() != "":   
      print("-------------------------------------------------------------------------------")
      print("Command: " + parmcommand)
      stdout=sftp.execute(parmcommand)
      for curstdout in stdout:
          print(curstdout.decode("utf-8"),end = '')

   # TODO - Need to parse return text for now. haven't figure this out return code yet with pysftp. 
   # Get return code from command 1 by using echo
   #if parmcommand.strip() != "":   
   #   stdout= sftp.execute("echo $?")
   #   # Only iterate first element which should be return code
   #   for curstdout in stdout:
   #       sshrtn=int(curstdout.decode("utf-8"))
   #       print(sshrtn)
   #       break;

   # Run command 2
   if parmcommand2.strip() != "":
      print("-------------------------------------------------------------------------------")
      print("Command2: " + parmcommand2)  
      stdout2=sftp.execute(parmcommand2)
      for curstdout in stdout2:
          print(curstdout.decode("utf-8"),end = '')
   
   # Run command 3
   if parmcommand3.strip() != "":
      print("-------------------------------------------------------------------------------")
      print("Command3: " + parmcommand3)  
      stdout3=sftp.execute(parmcommand3)
      for curstdout in stdout3:
          print(curstdout.decode("utf-8"),end = '')
   
   # Run command 4
   if parmcommand4.strip() != "":
      print("-------------------------------------------------------------------------------")
      print("Command4: " + parmcommand4)  
      stdout4=sftp.execute(parmcommand4)
      for curstdout in stdout4:
          print(curstdout.decode("utf-8"),end = '')
   
   # Run command 5
   if parmcommand5.strip() != "":
      print("-------------------------------------------------------------------------------")
      print("Command5: " + parmcommand5)  
      stdout5= sftp.execute(parmcommand5)
      for curstdout in stdout5:
          print(curstdout.decode("utf-8"),end = '')
 
   print("-------------------------------------------------------------------------------")
                        
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
