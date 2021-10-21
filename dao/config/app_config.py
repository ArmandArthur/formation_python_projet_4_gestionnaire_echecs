#!/usr/bin/env python
# coding: utf-8

class AppConfig:
    liste_config = dict(player='datas/players.json', 
    tournament='datas/tournaments.json')

    def __init__(self, table):
        self.table = table

    def config(self):
        return self.liste_config[self.table]
