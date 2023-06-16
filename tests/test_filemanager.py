#!/usr/bin/env python
# encoding: utf-8

import unittest
import tempfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from pigepy.filemanager import FileManager

class FileManagerTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.file_manager = FileManager(self.temp_dir, "%Y-%m-%d")
        # Print the created directories
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_create_dir(self):
        # Set the desired number of days
        days = 1
        
        # Calculate the new directory date
        now = datetime.now()
        new_dir_date = now - timedelta(days=days)
        new_dir = new_dir_date.strftime("%Y-%m-%d")
        
        # Call the createDir method
        self.file_manager.createDir({"days": days})
        
        # Print the created directories
        print("Created directories:")
        for path in Path(self.temp_dir).iterdir():
            if path.is_dir():
                print(path)
        

    def test_remove_old_directories(self):
        # Create some test directories
        now = datetime.now()
        
        self.file_manager.createDir({"days": 1})
        
        today_dir = (now + timedelta(days=0)).strftime("%Y-%m-%d")
        new_dir = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Path(self.temp_dir, new_dir).mkdir()
        
        for i in range(30):
            old_dir = (now - timedelta(days=(i+1))).strftime("%Y-%m-%d")
            Path(self.temp_dir, old_dir).mkdir()
        
        # Print the created directories
        print("Created directories:")
        for path in Path(self.temp_dir).iterdir():
            if path.is_dir():
                print(path)

        # Call the method to remove old directories
        self.file_manager.pruneOldDirectories(days=6)

        # Check if the old directory is removed and the new directory is still there
        self.assertFalse(Path(self.temp_dir, old_dir).exists())
        self.assertTrue(Path(self.temp_dir, new_dir).exists())
        
        # Print the deleted directories
        print("directories:")
        for path in Path(self.temp_dir).iterdir():
            if path.is_dir():
                print(path)
            
if __name__ == '__main__':
    unittest.main()