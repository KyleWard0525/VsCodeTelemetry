"""

 This file is the main driver for VSCT

 kward
"""

import os,sys,time
import psutil
import pymongo
import setproctitle
from ProcMonitor import ProcMonitor
from VsCodeTelemetry import VsCodeTelemetry

# Set title of the python process
setproctitle.setproctitle("VsCodeTelemetry")

# Ensure mongoDB service is running
os.system("net start mongodb")

# Setup database connection
mongodb = pymongo.MongoClient("mongodb://localhost:27017/")

# Select database
db = mongodb.misc["VsCodeLog"]

telem = VsCodeTelemetry(db)



def main():   
    proc = ProcMonitor("Code.exe")
    logging = False
    
    # Run forever
    while True:
        # Check if program is running
        if proc.isProcRunning() and not logging:
            telem.startCodeTimeLog()
            logging = True
        else:
            logging = False
            time.sleep(1)
            
if __name__ == "__main__":
    main()