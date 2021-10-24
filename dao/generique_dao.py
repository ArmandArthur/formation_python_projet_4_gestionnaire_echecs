#!/usr/bin/env python
# coding: utf-8

from tinydb import TinyDB, Query

from config.app_config import AppConfig


from pathlib import Path
import os.path 

from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

serialization = SerializationMiddleware(JSONStorage)
serialization.register_serializer(DateTimeSerializer(), 'TinyDate')


class GeneriqueDao:

    def __init__(self, table):
        self.app_config = AppConfig(table)
        self.path_folder_datas = 'datas'
        self.path_datas = self.app_config.config()
        self.path_file = self.path_folder_datas+'/'+self.path_datas

        # Create FOLDER
        Path(self.path_folder_datas).mkdir(parents=True, exist_ok=True)

        # Create FILE if no exists
        if os.path.exists(self.path_file) is False: 
            open(self.path_file, "w")

        # Init TinyDB
        self.db = TinyDB(self.path_file, sort_keys=True, indent=4, storage=serialization)

    def add(self, datas):
        return self.db.insert(datas)
