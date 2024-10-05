"""

 This file is the main driver for VSCT

 kward
"""

import os
import pymongo
import setproctitle
from VsCodeTelemetry import VsCodeTelemetry

# Set title of the python process
setproctitle.setproctitle("VsCodeTelemetry")

# Ensure mongoDB service is running
os.system("net start mongodb")

# Setup database connection
mongodb = pymongo.MongoClient("mongodb://localhost:27017/")

# Select database
db = mongodb.misc["VsCodeLog"]

def main():   
    telem = VsCodeTelemetry(db)
    telem.start()
            
if __name__ == "__main__":
    main()