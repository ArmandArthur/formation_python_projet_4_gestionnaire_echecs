#!/usr/bin/env python
# coding: utf-8

class MenuSortPlayersView:
    def __init__(self):
        self.questions = {}

    def sort_players(self):
        self.questions["playersSort"] = "Sort by (separated by commats) :"
        return self.questions
