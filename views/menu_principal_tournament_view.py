#!/usr/bin/env python
# coding: utf-8

class MenuPrincipalTournamentView:
    def __init__(self):
        self.questions = {}

    def questions_tournament(self):
        self.questions["tournamentCreate"] = "1) Create tournament"
        self.questions["tournamentStart"] = "2) Start/Continue a tournament"
        self.questions["tournamentList"] = "3) Tournaments list"
        return self.questions
