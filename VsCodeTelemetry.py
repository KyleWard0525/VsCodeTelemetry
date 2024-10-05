"""
This file is the main api for the app 

kward
"""
import time
import psutil
import pymongo
import pymongo.database

class VsCodeTelemetry:
    
    def __init__(self, db: pymongo.database.Database):
        # Create object for time logging
        self.time_log = {
            "name": "CodeTime",
            "total_time": 0,        #   Total time alive (in seconds); Carries across sessions
            "total_hours": 0,       #   Total time alive (in hours)
            "start_timestamp": 0    #   Date the program was first started [MM:DD:YYYY_HHMMSS]
        }

        # Set database
        self.db = db

        # Target process names
        self.target_process_names = ["Code.exe", "Code - Insiders.exe", "devenv.exe"]
        self.target_proc_start_time = 0

        # Set process monitor interval
        self.monitor_interval = 60

    def load_from_database(self) -> None:
        """
        Load total time from the database
        """
        # Check if load was successful
        if not self.db.find_one({"name": self.time_log["name"]}):
            # Set start timestamp
            self.time_log["start_timestamp"] = time.strftime("%m/%d/%Y %H:%M:%S")

            # Create entry in the database
            self.db.insert_one(self.time_log)
        else:
            self.time_log = self.db.find_one({"name": self.time_log["name"]})

        # Check if the start timestamp exists
        if not "start_timestamp" in self.time_log:
            # Set start timestamp
            self.time_log["start_timestamp"] = time.strftime("%m/%d/%Y %H:%M:%S")

            # Update database
            self.save_to_database()
        elif not self.time_log["start_timestamp"]:
            # Set start timestamp
            self.time_log["start_timestamp"] = time.strftime("%m/%d/%Y %H:%M:%S")

            # Update database
            self.save_to_database()
        else:
            pass

    def save_to_database(self) -> None: 
        """
        Store total time back into the db
        """
        # Check if total time is an hour (3600s) or more
        if self.time_log["total_time"] >= 3600:
            # Convert total time to hours
            self.time_log['total_hours'] = self.time_log["total_time"] / 3600.0
            
        return self.db.find_one_and_update(
            # Select code time document
            filter={"name": self.time_log["name"]},
            
            # Update to be made
            update={
                "$set" : self.time_log
            }
        )

    def is_process_running(self, proc_name: str) -> bool:
        """
        Check if the selected process is running

        Args:
            proc_name (str): Name of the process to check

        Returns:
            bool: True if process is running
        """
        # Get list of currently running process
        procs_alive = psutil.process_iter()
        
        # Iterate through process and check name
        for proc in procs_alive:
            if proc.name() == proc_name:
                return True
            
        return False

    def start(self):
        """
         Start the session timer
        """
        # Load total time from the database
        self.load_from_database()

        # Run forever
        while True:
            proc_running = False
            # Check if either vscode processes are running
            # Give priority to vscode insiders by checking it first
            for proc_name in self.target_process_names:
                if self.is_process_running(proc_name):
                    # Check if process start time has been set
                    if self.target_proc_start_time == 0:
                        self.target_proc_start_time = time.time()
                    proc_running = True
                    break   
            
            # Check if any of the target processes are running
            if proc_running:
                # Check if the difference between the current time and the process start time is less than the monitor interval
                curr_time = time.time()
                if curr_time - self.target_proc_start_time < self.monitor_interval:
                    self.time_log["total_time"] += curr_time - self.target_proc_start_time
                else:
                    self.time_log["total_time"] += self.monitor_interval

                # Save changes to the database
                self.save_to_database()
                    
            # Sleep for the monitor interval
            time.sleep(self.monitor_interval)