#!/usr/bin/env python
# coding: utf-8

from tinydb import TinyDB
from tinydb.table  import Document

from config.app_config import AppConfig

from pathlib import Path
import os.path 
import json 


class GeneriqueDao:

    def __init__(self, item_type):
        # Init TinyDB
        self.db = TinyDB('datas/echecs.json', sort_keys=True, indent=4)
        self.table = self.db.table(item_type.__name__.lower()+'s')
        self.item_type = item_type

        self.items = {}
        self.max_id = 0

        for item_data in self.table:
            self.create_item(**item_data)

    def create_item(self, *args, **kwargs):
        
        if 'id' not in kwargs:
            kwargs['id'] = self.max_id + 1

        # instance
        item = self.item_type(*args, **kwargs)
        self.items[item.id] = item
        self.max_id = max(self.max_id, item.id)
        return item
    
    def update_item(self, instance_model):
        item =  instance_model.dict()
        self.items[item['id']] = instance_model
        return instance_model

    def save_item(self, id):
        item = self.find_by_id(id)
        self.table.upsert(Document(json.loads(item.json()), doc_id=id))
        # datas_json = datas.json()
        # datas_insert = json.loads(datas_json)
        # return self.table.insert(datas_insert)
    
    def all(self):
        return list(self.items.values())

    def find_by_id(self, id):
        return self.items[id]