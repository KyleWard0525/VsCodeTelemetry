"""
 This file is for the tracking operation of this application
 
 kward
"""

import time


class CodeTime:
    
    def __init__(self, db):
        self.seshStart = 0          #   Start of the session (in seconds)
        self.seshEnd = 0            #   End of the session (elapsed time in seconds)
        self.db = db
        
        # Create object for time logging
        self.time_log = {
            "name": "CodeTime",
            "total_time": 0,        #   Total time alive (in seconds); Carries across sessions
            "total_hours": 0       #   Total time alive (in hours)
        }
        
        
    def _load(self):
        """
        Load total time from the database
        """
        
        # Check if load was successful
        if not self.db.find_one({"name": self.time_log["name"]}):
            # Create entry in the database
            self.db.insert_one(self.time_log)
        else:
            self.time_log = self.db.find_one({"name": self.time_log["name"]})
        
        
    def _store(self):
        """
        Store total time back into the db
        """
        # Check if 
        
        # Check if total time is an hour (3600s) or more
        if self.time_log["total_time"] >= 3600:
            # Convert total time to hours
            self.time_log['total_hours'] = self.time_log["total_time"] / 3660.0
            
            
        update = {}
        
        # Check if total_hours should be updated in the DB
        if self.time_log['total_hours'] >= 0:
            update = {
                "$set" : {"total_time" : round(self.time_log["total_time"],3),
                         "total_hours" : round(self.time_log["total_hours"],2)}
            }
        else:
            update = {
                "$set" : {"total_time" : round(self.time_log["total_time"],3)}
            }
        
        
        return self.db.find_one_and_update (
            # Select code time document
            filter={"name": self.time_log["name"]},
            
            # Update to be made
            update = update
        )
        
    def start(self):
        """
         Start the session timer
        """

        # Load data from DB
        self._load()


        # Set session start time
        self.seshStart = time.time()
        
    def stop(self):
        """
         End the session time and store the results in the db
        """
        
        # Compute time elapsed in seconds
        self.seshEnd = time.time()
        session_time = self.seshEnd - self.seshStart
        
        # Increment total time by session time
        self.time_log["total_time"] += session_time
        
        if self._store():
            print("\nSession log saved!")
        else:
            print("\nFailed to save data to the DB")
        
        # Clear variables
        self.seshStart = 0
        self.seshEnd = 0