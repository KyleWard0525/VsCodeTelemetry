"""
This file is for monitoring processes that are running on the machine
    
kward
"""

import os, sys, time
import psutil

class ProcMonitor:
    
    def __init__(self, procName):
        """
        Initialize process monitor

        Args:
            procName (str): Name of the process to monitor
        """
        self.proc = procName    # Set name of the process to monitor
        
        
    def isProcRunning(self):
        """
        Check if the selected process is running

        Returns:
            bool: True if process is running
        """
        # Get list of currently running process
        procs_alive = psutil.process_iter()
        
        # Iterate through process and check name
        for proc in procs_alive:
            if proc.name() == self.proc:
                return True
            
        return False
    
    
    def monitor(self):
        print(f"\nProcess Monitor on '{self.proc}' started")
        if self.isProcRunning():
            while self.isProcRunning():
                # Do nothing
                time.sleep(1)
        else:
            print(f"\n\nERROR in ProcMonitor.monitor(): process '{self.proc}' is not currently running.\n")
        
        # Return when process dies
        return -1
        
    