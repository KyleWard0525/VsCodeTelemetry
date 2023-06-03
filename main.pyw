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

# Create process monitors
procmon_vscode_std = ProcMonitor("Code.exe")
procmon_vscode_insiders = ProcMonitor("Code - Insiders.exe")
telem = VsCodeTelemetry(db)


def main():   
    logging = False
    
    # Run forever
    while True:
        # Check if either vscode processes are running
        # Give priority to vscode insiders by checking it first
        if procmon_vscode_insiders.isProcRunning() and not logging:
            telem.startCodeTimeLog(procmon_vscode_insiders)
            logging = True
        elif procmon_vscode_std.isProcRunning() and not logging:
            telem.startCodeTimeLog(procmon_vscode_std)
            logging = True
        else:
            logging = False
            time.sleep(1)
            
if __name__ == "__main__":
    main()