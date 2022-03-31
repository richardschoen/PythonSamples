#!/QOpenSys/pkgs/bin/python3
#------------------------------------------------
# Script name: pyhellotodb.py
#
# Description: 
# This script is a template for writing a Python script that will
# output all the selected into in to a database table so the 
# info can be analyzed or accessed from any other app, including RP, CL or COBOL.
#
# Parameters
# --parm1 - Example parm1 - Not really used, but here as a parm pattern
# --parm2 - Example parm2 - Not really used, but here as a parm pattern
# --parm3bool - Example parm3 - Not really used, but here as a boolean parm pattern
#
# Testing commnad line - CLI
# python3 pyhellotodb.py --parm1 AA --parm2 BB --outputtable tmp.aa         
#
# Process steps:
# -Create/replace DB2 table and clear it
# -Insert a couple records
#------------------------------------------------

import argparse
import ibm_db_dbi as db2
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
insertcount=0

#Output messages to STDOUT for logging
print("-------------------------------------------------------------------------------")
print("Hello output to database table/outfile")
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

def insert_hellodb(cursor,table,hvalue1,hvalue2,hintvalue3):
    #----------------------------------------------------------
    # Function: insert_hellodb
    # Desc: Insert new record into hellodb outfile table
    # :return: Result value from query
    #----------------------------------------------------------
    try:
       # Create the SQL statement 
       sql = """insert into %s (HVALUE1,HVALUE2,HINTVALUE3) VALUES('%s','%s',%s)""" % (table,hvalue1,hvalue2,hintvalue3)
       # Insert the record
       # Note: self parm not needed for execute when internal class function called
       rtnexecute=cursor.execute(sql)
       # Return result value
       return rtnexecute
    except Exception as e:
       print(e)  
       return -2 # return -2 on error 

def drop_table(cursor,table):
    #----------------------------------------------------------
    # Function: drop_table
    # Desc: Drop the selected table
    # :return: Result value from query
    #----------------------------------------------------------
    try:
       # Create the SQL statement 
       sql = """drop table %s""" % (table)
       # Drop the table
       # Note: self parm not needed for execute when internal class function called
       rtnexecute=cursor.execute(sql)
       if rtnexecute == True:
          print("Table " + table + " was dropped" ) 
       # Return result value
       return rtnexecute
    except Exception as e:
       print(e)  
       return -2 # return -2 on error 

def create_hellodb(cursor,table):
    #----------------------------------------------------------
    # Function: create_hellodb
    # Desc: Create the hellodb outfile table
    # :return: Result value from query
    #----------------------------------------------------------
    try:
       # Create the SQL statement 
       sql = """create table %s (HVALUE1 VARCHAR(256),HVALUE2 VARCHAR(256),HINTVALUE3 int)""" % (table)
       # Create the table
       # Note: self parm not needed for execute when internal class function called
       rtnexecute=cursor.execute(sql)
       if rtnexecute == True:
          print("Table " + table + " was created" ) 
       # Return result value
       return rtnexecute       
    except Exception as e:
       print(e)  
       return -2 # return -2 on error 

def execute_clcommand(cursor,clcommand):
    #----------------------------------------------------------
    # Function: execute_clcommand
    # Desc: Run IBM i CL Command
    # :return: Result value from query
    #----------------------------------------------------------
    try:
       # Create the SQL statement 
       clwork = """CALL QSYS2.QCMDEXC('%s')""" % (clcommand)
       # Run the CL command
       # Note: self parm not needed for execute when internal class function called
       rtnexecute=cursor.execute(clwork)
       # Return result value
       return rtnexecute
    except Exception as e:
        print(e)  
        return -2 # return -2 on error 

#------------------------------------------------
# Main script logic
#------------------------------------------------
try: # Try to perform main logic

      # Set up the command line argument parsing
      # If the parse_args function fails, the program will
      # exit with an error 2. In Python 3.9, there is
      # an argument to prevent an auto-exit
      parser = argparse.ArgumentParser()
      parser.add_argument('--parm1', required=True,help="This is example parm1 that is required")
      parser.add_argument('--parm2', required=True,help="This is example parm2 that is required")
      parser.add_argument('--parm3bool',default=False,required=False,help="This is example bool parm3 that is not required")   
      parser.add_argument('--outputtable', required=True,help="Output DB2 table (LIBRARY.FILENAME)")

      # Parse the command line arguments
      args = parser.parse_args()

      # Convert args to variables
      parm1=args.parm1
      parm2=args.parm1
      parm3bool=args.parm3bool
      outputtable=args.outputtable

      # Connect to DB2 database
      conn = db2.connect()
      # No committment control for temp tables
      conn.set_option({ db2.SQL_ATTR_TXN_ISOLATION:
                        db2.SQL_TXN_NO_COMMIT })            
      # Enable auto-commit
      ##conn.set_autocommit(True)
      # Create cursor which we will use for DB actions
      cur1 = conn.cursor()

      # Drop temp outfile table if it exists
      rtndrop=drop_table(cur1,outputtable)
      print(f"Drop: {rtndrop}")

      # Create temp outfile table if it does not exist
      rtncreate=create_hellodb(cur1,outputtable)
      print(f"Create: {rtncreate}")
      # Bail out if we cannot create
      if (rtncreate != True):
         raise Exception(f"Unable to create table {outputtable}. Process cancelled.")          

      # Output parm values - totally up to you, but I like to log some values in STDOUT logging
      print(f"Parameter 1: {parm1}")
      print(f"Parameter 2: {parm2}")
      print(f"Parameter 3 boolean: {parm3bool}")
      print(f"Output table: {outputtable}")      

      # Do some work. In our example we will just insert 2 sample records

      # Insert 2 records with vals from parm1 and parm2
      for counter in range(0,2):

          #Insert record to outfile now
          rtnins=insert_hellodb(cur1,outputtable,parm1,parm2,str(counter))

          # Make record insert succeeds
          if (rtnins != True ):
             raise Exception(f"Error inserting file/link record to  {outputtable}. Process cancelled.")          

          # Increment insert counter. Again totally optional usage but I like to count records
          insertcount = insertcount + 1 

      # Close DB2 connection
      conn.close()

      # Print file and dir counts
      print(f"Insert count: {insertcount} records inserted to output table {outputtable}")

      # Set success info
      exitcode=0
      exitmessage="Completed successfully"

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
    print(f"ExitCode: {exitcode}")
    print(f"ExitMessage: {exitmessage}")
    print("End of Main Processing - " + time.strftime("%H:%M:%S"))
    print("-------------------------------------------------------------------------------")
    
    # Exit the script now
    sys.exit(exitcode) 

