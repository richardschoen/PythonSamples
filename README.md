# PythonSamples
Python Samples

This repository will be used for miscellaneous Python samples for all platforms including"
***Windows, Linux, Mac and IBM i/AS400**
* Main
    * `cmdlineparmsample1.py` - This is a template command line CLI script that utilizes argparse to parse command line arguments and then do some work. The main line logic is wrapped by try/catch for clean error handling and exit on error.

* General
    * `hello.py` - Tiny hello world example
    * `hellotemplate.py` - Python script template with standard error handling built in. Fails nicely and also returns non-zero error code on failure.

* IBM i
    * `ibmi_d_to_dt.py` - Convert IBM i date CYYMMDDHHMMSS to Python datetime
    * `ibmintptimeupdate.py` - Use remote NTP server and CHGSYSVAL to update system time value QTIME.   
    * `pybackgroudsample1.py` - Sample background polling process script. 
    * `pyhellotodb.py` Sample Python template to do some Python work and write to a sample outfile.DB2 table
    * `pyitool01.py` Call CL program via iToolkit and XMLSERVICE.
    * `pypgmcall001.py` - Call CL program via iToolkit and XMLSERVICE.
    * `pydbtoexcel.py` - Run SQL to extract IBM i DB2 data to an Excel file
    * `pyodbcconnectiontest.py` - IBM i ODBC connection tester. Use to test native ODBC connection.
    * `pysftpdownload.py` - Sample SFTP file download using pysftp. Now supports user/password or user/privatekeyfile.
    * `pysftpupload.py` - Sample SFTP file upload using pysftp. Now supports user/password or user/privatekeyfile.
