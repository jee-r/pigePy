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
        
        self.file_format = "%Y-%m-%d_%Hh-%Mm-%Ss"
        self.directory_format = "%Y/%m/%d"
        
        self.file_manager = FileManager(self.temp_dir, self.directory_format)

        # Print the created directories
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def create_empty_file(self, file_path):
        with open(file_path, 'w'):
            pass

    def test_create_dir(self):
        # Set the desired number of days
        days = 1
        
        # Calculate the new directory date
        now = datetime.now()
        today_dir = now.strftime(self.directory_format)
        new_dir_date = now + timedelta(days=days)
        new_dir = new_dir_date.strftime(self.directory_format)
        
        # Call the createDir method
        self.file_manager.createDir({"days": days})

        # Print the created directories
        print("Created directories:")
        for path in Path(self.temp_dir).rglob("*"):
        #    if path.is_dir():
            print(path)
        
        self.assertTrue(Path(self.temp_dir, today_dir).exists())
        self.assertTrue(Path(self.temp_dir, new_dir).exists())

    def test_remove_old_directories(self):
        # Create some test directories
        now = datetime.now()
        directory_format = "%Y/%m/%d"
        file_format = "%Hh-%Mm-%Ss"
        year_range = 2
        month_range = 6
        day_range = 8
        hour_range = 6
        retention_days = 4 
        retention = {
            "days": 4,
            "hours": 0,
            "minutes": 0
        }

        total_files_created = (((hour_range * day_range)*month_range)*year_range)
        # self.file_manager.createDir({"days": 1})
        
        today_diddr = (now + timedelta(days=0)).strftime("%Y-%m-%d")
        new_dir = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Path(self.temp_dir, new_dir).mkdir()
        
        for year in range(year_range):
            coef_year = year * 365
            for month in range(month_range):
                coef_month = month * 30 
                for day in range(day_range):
                    directory_name = (now - timedelta(days=(day + 1 + coef_year + coef_month))).strftime(directory_format)
                    Path(self.temp_dir, directory_name).mkdir(parents=True, exist_ok=True)
                    for hour in range(hour_range):
                        file_name = (now - timedelta(hours=hour)).strftime(file_format)
                        file_path = Path(self.temp_dir, directory_name, file_name + ".mp3")
                        self.create_empty_file(file_path)

        files_created_counter = 0
        
        for file in Path(self.temp_dir).rglob('*'):
            if file.is_file():
                files_created_counter += 1

        print("Total files created:", files_created_counter)                            

        # Call the method to remove old directories
        self.file_manager.prune_old_files(directory_format, file_format, False, retention)
        
        files_not_deleted_counter = 0
        
        for file in Path(self.temp_dir).rglob('*'):
            if file.is_file():
                print(file)
                files_not_deleted_counter += 1
        
        print("Total files not deleted:", files_not_deleted_counter)
        
        self.assertTrue((files_not_deleted_counter == (retention_days * hour_range) - hour_range))
        
            
    def test_prune_old_files_nosubdir(self):
        now = datetime.now()
        file_format = "%Y-%m-%d_%Hh-%Mm-%Ss"
        directory_format = "%Y/%m/%d"
        year_range = 2
        month_range = 6
        day_range = 8
        hour_range = 6
        retention_days = 4
        retention = {
            "days": 4,
            "hours": 0,
            "minutes": 0
        }
        
        # print("Prune: Created files")
        for day in range(day_range):
            for hour in range(hour_range):
                file_name = (now - timedelta(days=(day+1), hours=hour)).strftime(file_format)
                file_path = Path(self.temp_dir, file_name)
                self.create_empty_file(file_path)
        
        files_created_counter = 0
        
        for file in Path(self.temp_dir).rglob('*'):
            if file.is_file():
                files_created_counter += 1

        print("NoSubDir Total files created:", files_created_counter)

        # Call the method to remove old directories
        self.file_manager.prune_old_files("", file_format, True, retention)
        
        files_not_deleted_counter = 0

        for file in Path(self.temp_dir).rglob('*'):
            if file.is_file():
                # print(file)
                files_not_deleted_counter += 1
        
        print("NoSubDir Expected Total files not deleted:", files_not_deleted_counter)
        
        self.assertTrue((files_not_deleted_counter == (retention_days * hour_range) - hour_range))

if __name__ == '__main__':
    unittest.main()