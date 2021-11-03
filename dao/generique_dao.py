#!/usr/bin/env python
# coding: utf-8

from tinydb import TinyDB

from config.app_config import AppConfig

from pathlib import Path
import os.path 
import json 


class GeneriqueDao:

    def __init__(self, table):
        self.app_config = AppConfig()
        self.path_folder_datas = 'datas'
        self.path_datas = self.app_config.config()
        self.path_file = self.path_folder_datas+'/'+self.path_datas

        # Create FOLDER
        Path(self.path_folder_datas).mkdir(parents=True, exist_ok=True)

        # Create FILE if no exists
        if os.path.exists(self.path_file) is False: 
            open(self.path_file, "w")

        # Init TinyDB
        self.db = TinyDB(self.path_file, sort_keys=True, indent=4)
        self.table = self.db.table(table)

    def add(self, datas):
        datas_json = datas.json()
        datas_insert = json.loads(datas_json)
        return self.table.insert(datas_insert)
    
    def all(self):
        return self.table.all()
