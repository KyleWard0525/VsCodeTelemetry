"""
 This file will server as the DOS command for querying and displaying
 VSCT metrics in CMD or Powershell
 
 kward
"""

import os
import sys
import json
import pymongo

# Setup database connection
mongodb = pymongo.MongoClient("mongodb://localhost:27017/")

# Select database
db = mongodb.misc["VsCodeLog"]


def get_metrics():
    """
    Query VS Code metrics from the db
    """    
    
    time_metrics = db.find_one({"name" : "CodeTime"})
    
    return {
        "total_time" : time_metrics["total_time"],
        "total_hours" : time_metrics["total_hours"]
    }


def format_output():
    """
     Format output to be sent to stdout
    """
    
    # Load metrics from db
    metrics = get_metrics()
    linelen = 40
    
    output = f"""
    
    \t\tVS Code Telemetry:
    {"-"*linelen}\n
    
    Total time spent in VS Code: {metrics["total_hours"]} hours
    
    """
                
    return output

def main():
    # Print formatted output string
    print(format_output(), file = sys.stdout)

main()