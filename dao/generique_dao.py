#!/usr/bin/env python
# coding: utf-8

from tinydb import TinyDB, Query

from config.app_config import AppConfig


class GeneriqueDao:

    def __init__(self, table):
        self.app_config = AppConfig(table)
        self.path_datas = self.app_config.config()
        self.db = TinyDB(self.path_datas)
        self.add({'display_id':'123', 'tags':['a', 'abc', 'xyz'], 'title': 'num'})

    def add(self, datas):
        return self.db.insert(datas)

if __name__ == "__main__":
    GeneriqueDao('player')