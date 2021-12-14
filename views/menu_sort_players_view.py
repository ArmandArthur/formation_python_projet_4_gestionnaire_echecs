#!/usr/bin/env python
# coding: utf-8

class MenuSortPlayersView:
    def __init__(self):
        self.questions = {}

    def sort_players(self):
        """
            Dict des modes possibles

            @return: Le dict
        """
        self.questions["playersSort"] = "Sort by (separated by commats) :"
        return self.questions
