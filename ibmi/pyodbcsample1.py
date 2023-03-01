#!/QOpenSys/pkgs/bin/python3
#------------------------------------------------
# Script name: pyodbcsample1.py
#
# Description: 
# This script is a sample to read an IBM i table using 
# pyodbc and the IBM i Access ODBC Driver. 
#
# Parameters:
# None 
#
# Pip packages needed:
# pip3 install pyodbc
#
# Returns:
# Exits with 0 on success or 99 on errors.
# This allows us to communicate back to command line with an appropriate return code.
#------------------------------------------------

#------------------------------------------------
# Imports
#------------------------------------------------
import pyodbc
import sys
import time
import traceback

#------------------------------------------------
# Script initialization
#------------------------------------------------

exitcode=0 #Init exitcode
exitmessage='' #init final exit message
dashes= '-----------------------------------------------------' #I like to output dashes as separators in stdout.

# Set connection string. Normally this might be stored in a config file. 
# Run natively on IBM i as current user with *LOCAL DSN created by IBM i Access ODBC install
odbcconnstring="DSN=*LOCAL;CommitMode=0;EXTCOLINFO=1;"
# Run as specific user on selected system with soft coded connection string
#odbcconnstring= "Driver={IBM i Access ODBC Driver};System=1.1.1.1;Uid=USER01;Pwd=PASS01;CommitMode=0;EXTCOLINFO=1;"

# Output messages to STDOUT for logging
print(dashes)
print("Start of Main Processing - " + time.strftime("%H:%M:%S"))

#------------------------------------------------
# Main script logic
#------------------------------------------------
try: # Try to perform main logic

   # Connect to the database and get a cursor
   print("Connecting to IBM i database via PYODBC - " + time.strftime("%H:%M:%S"))
   conn = pyodbc.connect(odbcconnstring)
   cursor = conn.cursor()
   
   # Run the db query
   print("Querying IBM i database via PYODBC - " + time.strftime("%H:%M:%S"))
   cursor.execute("SELECT * FROM qiws.qcustcdt")
   
   # Output the data
   print("Outputting query results - " + time.strftime("%H:%M:%S"))
   for row in cursor.fetchall():
       print(row)
   
   # Close connection
   conn.close()
   
   # Set success info
   exitcode=0
   exitmessage='Completed successfully'

#------------------------------------------------
# Catch and Handle Exceptions
#------------------------------------------------
except: 
   exitcode=99
   exitmessage='Error occurred'
   print('Traceback Info')
   traceback.print_exc()
#------------------------------------------------
# Always perform final processing
#------------------------------------------------
finally: # Final processing

    # Do any final code and exit now
    print('ExitCode:' + str(exitcode))
    print('ExitMessage:' + exitmessage)
    print("End of Main Processing - " + time.strftime("%H:%M:%S"))
    print(dashes)
    
    # Exit the script now
    sys.exit(exitcode) 
