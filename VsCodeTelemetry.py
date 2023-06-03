"""
This file is the main api for the app 

kward
"""

from CodeTime import CodeTime
from ProcMonitor import ProcMonitor


class VsCodeTelemetry:
    
    def __init__(self, db):
        self.codeTime = CodeTime(db)

    def startCodeTimeLog(self, procmon: ProcMonitor):
        # Start timer
        self.codeTime.start()
        
        # Monitor process
        while procmon.monitor() != -1:
            if not procmon.isProcRunning():
                break
        
        # Stop timer and save session time to the db
        self.codeTime.stop()