#!/usr/bin/python
# ------------------------------------------------
# Script name: pypgmcall001.py
#
# Description:
# This script will connect to a local IBM i system
# via XMLSERVICE and set the library and call a program
# named PYPGM001C in library PYSAMPLES.
# The program uses iToolkit for connectivity.
# The program call will receive 2 return parameter
# values which can then be used as needed.
# In our example we just output them.
#
# CL sample is in:
# library PYSAMPLES, file: SOURCE, member: PYPGM001C
#
# Note: Make sure the Python3 iToolkit version is 1.6.1.0
# or above. Othewise errors may occur.
#
# Incoming Parameters
# None
# -------------------------------------------------------------------------
#
# CL Sample program
#
#/****************************************************/            
#/* Program: PYPGM001C                               */            
#/* Desc . : Test Program to Return Parameters       */            
#/*          We set a return message and also        */            
#/*          increment and return the balance.       */            
#/*          This sample obviously does no database  */            
#/*          updating but illustrates passing parms. */            
#/****************************************************/            
#             PGM        PARM(&RTNMSG &AMOUNT)                     
#                                                                  
#             DCL        VAR(&RTNMSG) TYPE(*CHAR) LEN(50)          
#             DCL        VAR(&AMOUNT) TYPE(*DEC) LEN(15 2)         
#             DCL        VAR(&INCREMENT) TYPE(*DEC) LEN(15 2) +    
#                          VALUE(1000000.00)                       
#                                                                  
#/* Program level monitor to handle any unhandled errors */        
#/* We don't want out app throwing QSYSOPR messages.     */          
#             MONMSG     MSGID(CPF0000) EXEC(GOTO CMDLBL(ERRORS))    
#                                                                    
#/* Increment balance based on passed in amount */                   
#             CHGVAR     VAR(&AMOUNT) VALUE(&INCREMENT + &AMOUNT)    
#                                                                    
#/* Set return message and return */                                 
#             CHGVAR     VAR(&RTNMSG) VALUE(&AMOUNT)                 
#             CHGVAR     VAR(&RTNMSG) VALUE('Thank you for your +    
#                          business')                                
#                                                                    
#             RETURN                                                 
#                                                                    
#/* Set error return message and return */                           
#ERRORS:                                                             
#             CHGVAR     VAR(&RTNMSG) VALUE('ERROR: Errors occurred +
#                          during processing')                       
#             CHGVAR     VAR(&AMOUNT) VALUE(-99999.00)     
#                                                          
#             ENDPGM                                       						  
# -------------------------------------------------------------------------

# ------------------------------------------------
# Imports
# ------------------------------------------------
from itoolkit import *
from itoolkit.transport import DatabaseTransport
import ibm_db_dbi
import sys
from sys import platform
import os
import time
import traceback

# ------------------------------------------------
# Declare any script level work variables
# ------------------------------------------------
exitcode=0
exitmessage=""

# ------------------------------------------------
# Main script logic
# ------------------------------------------------
try:  # Try to perform main logic

      # Connect to the IBM system and instantiate iToolkit
      # We will run a CL command and a program call in tandem.
      conn = ibm_db_dbi.connect()
      itransport = DatabaseTransport(conn)
      itool = iToolKit()

      #Add PYSAMPLES to library list
      itool.add(iCmd('addlible', 'ADDLIBLE PYSAMPLES'))

      #Add program call to PYPGM001C in PYSAMPLES
      itool.add(
          iPgm('pypgm001c', 'PYPGM001C')
              .addParm(iData('RTNMSG', '50a', 'a'))
              .addParm(iData('AMOUNT', '15p2', '33.33'))
      )

      # Perform xmlservice program call
      itool.call(itransport)

      # Get addlible output
      addlible = itool.dict_out('addlible')
      if 'success' in addlible:
          print(addlible['success'])
      else:
          raise Exception("Add library list error occurred.")

      pypgm001c = itool.dict_out('pypgm001c')
      if 'success' in pypgm001c:
          print(pypgm001c['success'])
          print("Return parameter values:")
          print("RTNMSG: " + pypgm001c['RTNMSG'])
          print("AMOUNT: " + pypgm001c['AMOUNT'])
      else:
          raise Exception("Program call error:" + pypgm001c['error'])

      # Set success info
      exitcode = 0
      exitmessage = 'Completed successfully'

# ------------------------------------------------
# Handle Exceptions
# ------------------------------------------------
except Exception as ex:  # Catch and handle exceptions
      exitcode = 99  # set return code for stdout
      exitmessage = str(ex)  # set exit message for stdout
      print('Traceback Info')  # output traceback info for stdout
      traceback.print_exc()

  # ------------------------------------------------
  # Always perform final processing
  # ------------------------------------------------
finally:  # Final processing
      # Do any final code and exit now
      # We log as much relevent info to STDOUT as needed
      print('ExitCode:' + str(exitcode))
      print('ExitMessage:' + exitmessage)

      # Exit the script now
      sys.exit(exitcode)
