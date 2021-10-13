#!/QOpenSys/pkgs/bin/python3
#-------------------------------------------------------------------------
# Script : pyitool01.py
# Author: Richard Schoen
# Date written: 10/13/2021
# Purpose: Use itoolkit to call a CL program and return a message.  
#          Parm 1 - 50 character field for return message. 
#          Parm 2 - 15,2 packed field. Pass amount in to call.  
#          
#-------------------------------------------------------------------------
# Date       Programmer      Description                                   
#-------------------------------------------------------------------------
# 10/13/2021 Richard Schoen  Original code synthesized from itjungle link
#                            by Mike Larsen.                                 
#                                                                     
# Links: 
# https://www.itjungle.com/2020/03/30/guru-calling-rpg-programs-from-python-part-1
# https://python-itoolkit.readthedocs.io/en/latest/examples.html
#------------------------------

# Listed below is sample CL Program: PYITOOL01.CLP
# Enter this in to QCLSRC in QGPL and compile it. (Or your favorite development library) 
"""
/****************************************************/            
/* Program: PYITOOL01                               */            
/* Desc . : Test Program to Return Parameters       */            
/*          We set a return message and also        */            
/*          increment and return the balance.       */            
/*          This sample obviously does no database  */            
/*          updating :-)                            */            
/****************************************************/            
             PGM        PARM(&RTNMSG &AMOUNT)                     
                                                                  
             DCL        VAR(&RTNMSG) TYPE(*CHAR) LEN(50)          
             DCL        VAR(&AMOUNT) TYPE(*DEC) LEN(15 2)         
             DCL        VAR(&INCREMENT) TYPE(*DEC) LEN(15 2) +    
                          VALUE(1000000.22)                       
             MONMSG     MSGID(CPF0000) EXEC(GOTO CMDLBL(ERRORS))  
/* INCREMENT BALANCE BASED ON PASSED AMOUNT */                       
             CHGVAR     VAR(&AMOUNT) VALUE(&INCREMENT + &AMOUNT)     
                                                                     
/* SET RETURN MESSAGE */                                             
             CHGVAR     VAR(&RTNMSG) VALUE(&AMOUNT)                  
             CHGVAR     VAR(&RTNMSG) VALUE('Thank you for your +     
                          business')                                 
                                                                     
             RETURN                                                  
ERRORS:                                                              
             CHGVAR     VAR(&RTNMSG) VALUE('ERROR: Errors occurred + 
                          during processing')                        
             MONMSG     MSGID(CPF0000)                               
             CHGVAR     VAR(&AMOUNT) VALUE(-99999.00)                
             MONMSG     MSGID(CPF0000)                               
                                                                     
             ENDPGM                                                               
"""

#------------------------------------------------
# Imports
#------------------------------------------------
import sys
from sys import platform
import os
import time
import traceback
import datetime as dt
from itoolkit import *
from itoolkit.lib.ilibcall import *
from itoolkit.transport import DatabaseTransport
from itoolkit.transport import DirectTransport
import ibm_db_dbi

#------------------------------------------------
# Script initialization
#------------------------------------------------

# Initialize or set variables
exitcode=0 #Init exitcode
exitmessage=''

#------------------------------------------------
# Main script logic
#------------------------------------------------
try: # Try to perform main logic
  
   #Output messages to STDOUT for logging
   print("-------------------------------------------------------------------------------")
   print("Calling IBM i Program with Parameters")
   print("Start of Main Processing - " + time.strftime("%H:%M:%S"))
   print("OS:" + platform)
   print(" ")
       
   # Use libcall transport - libcall seems to have a bug that is PTF related. See link below:
   # https://python-itoolkit.readthedocs.io/en/latest/api.html#module-itoolkit.transport 
   # itransport = iLibCall()
   # itool = iToolKit()
  
   # Use DirectTransport transport - Suffers from same issue as libcall 
   # itransport = DirectTransport()
   # itool = iToolKit()
  
   # Use Database transport
   conn = ibm_db_dbi.connect()
   itransport = DatabaseTransport(conn)
   itool = iToolKit()
  
   # Compiled the CL in library QGPL. You can use whatever library you have the program in
   itool.add(iCmd('addlible', 'addlible qgpl'))
  
   # Set up program call with 2 parms
   # RTNMSG   50a  - Used to return message only
   # AMOUNT   15p2 - Send in an sample dollar amount which will get incremented.   
   itool.add(
   iPgm('my_results','PYITOOL01')
     .addParm(iData('RTNMSG','50a',''))
     .addParm(iData('AMOUNT','15p2','100.00'))
   )
  
   # Call the program now
   itool.call(itransport)
  
   # Get results back in to a dictionary
   mypgm_results = itool.dict_out('my_results')
  
   # Print out the entire result dictionary
   print('Program call results:')   
   print(mypgm_results)
  
   # Note success or failure
   if 'success' in mypgm_results:
      # Output the results
      print('\n')
      print('Program call return info:')      
      print("Return message: ", mypgm_results['RTNMSG'])
      print("Status of the program call: ", mypgm_results['success'])
   
      # Set success info
      exitcode=0
      exitmessage="Program call completed normally." 
   else:
      # Raise error exception
      raise Exception('Error occurred when calling program.')
  

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
    print(' ')
    print('ExitCode:' + str(exitcode))
    print('ExitMessage:' + exitmessage)
    print("End of Main Processing - " + time.strftime("%H:%M:%S"))
    print("-------------------------------------------------------------------------------")
    
    # Exit the script now
    sys.exit(exitcode)  

