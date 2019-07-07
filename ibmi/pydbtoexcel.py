#!/usr/bin/python
#------------------------------------------------
# Script name: pydbtoexcel.py
#
# Description: 
# This script will operform an SQL query and export
# the results to an Excel file using Pandas
#
# Pip packages needed:
# pip3 install pandas
# pip3 install xlsxwriter
#
# Parameters
# P1=SQL query Ex: select * from qiws.qcustcdt
# P2=Output excel file. Ex: /tmp/excelfile.xlsx
# p3=Replace existing=True-replace, False-Do not replace
#------------------------------------------------

#------------------------------------------------
# Imports
#------------------------------------------------
import sys
from sys import platform
import os
import time
import traceback
import xlsxwriter
import pandas as pd

import ibm_db_dbi as db2 

#------------------------------------------------
# Script initialization
#------------------------------------------------

# Initialize or set variables
exitcode=0 #Init exitcode
exitmessage=''
parmsexpected=3;

#Output messages to STDOUT for logging
print("-------------------------------------------------------------------------------")
print("DB2 Query to Excel File")
print("Start of Main Processing - " + time.strftime("%H:%M:%S"))
print("OS:" + platform)

#------------------------------------------------
# Main script logic
#------------------------------------------------
try: # Try to perform main logic
   

   # Check to see if all required parms were passed
   if len(sys.argv) < parmsexpected + 1:
        raise Exception(str(parmsexpected) + ' required parms - [SQL Query] [Excel Output File] [Replace-True/False]. Process cancelled.')
   
   # Set parameter work variables from command line args
   parmscriptname = sys.argv[0] 
   parmsqlquery= sys.argv[1] 
   parmexcelfile= sys.argv[2]
   parmreplace= eval(sys.argv[3]) #replace-True/False
   print("SQL: " + parmsqlquery)
   print("Excel output file: " + parmexcelfile)
   print("Replace output file if found: " + str(parmreplace))

   # Check for Excel file in IFS and delete if found
   exists = os.path.isfile(parmexcelfile)
   if exists: 
      if parmreplace==True:
        os.remove(parmexcelfile)
      else:
        raise Exception('File ' + parmexcelfile + ' exists and replace not selected. Process cancelled.')

   # Connect to database using PASE DB2 driver
   conn = db2.connect()

   # Run SQL query via Pandas
   df = pd.read_sql(parmsqlquery,conn)

   # Export the DataFrame to Excel. 
   # Make sure index column with row number. (Inex=false)
   df.to_excel(parmexcelfile,index=False)
   
   # Check for file and make sure it exists now. Bail if not found.
   exists = os.path.isfile(parmexcelfile)
   if exists==False: 
        raise Exception('Output file ' + parmexcelfile + ' was not created. Process cancelled.')

   # Output return parm info in case user wants to know file name created from RPG/CL  
   print("RTNEXCELFILE:" + parmexcelfile)

   # Set success info
   exitcode=0
   exitmessage='Completed successfully'

#------------------------------------------------
# Handle Exceptions
#------------------------------------------------
except Exception as ex: # Catch and handle exceptions
   exitcode=99 # set return code for stdout
   exitmessage=str(ex) # set exit message for stdout
   print('Traceback Info') # output traceback info for stdout
   traceback.print_exc()        

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