#!/usr/bin/env python
# coding: utf-8

from tinydb import TinyDB, Query

from config.app_config import AppConfig


from pathlib import Path
import os.path


class GeneriqueDao:

    def __init__(self, table):
        self.app_config = AppConfig(table)
        self.path_folder_datas = '../datas/'
        self.path_datas = self.app_config.config()
        self.path_file = self.path_folder_datas+self.path_datas

        # Create FOLDER
        Path(self.path_folder_datas).mkdir(parents=True, exist_ok=True)

        #Create FILE if no exists
        if os.path.exists(self.path_file) is False: 
            open(self.path_file, "w")
        
        self.db = TinyDB(self.path_file, sort_keys=True, indent=4)
        #self.add({'display_id':'123', 'tags':['a', 'abc', 'xyz'], 'title': 'num'})

    def add(self, datas):
        return self.db.insert(datas)

# if __name__ == "__main__":
#     GeneriqueDao('player')