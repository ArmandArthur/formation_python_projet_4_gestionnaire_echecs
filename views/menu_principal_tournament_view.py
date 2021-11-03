#!/usr/bin/env python
# coding: utf-8

class MenuPrincipalTournamentView:
    def __init__(self):
        self.questions = {}

    def questions_tournament(self):
        self.questions["tournamentCreate"] = "1) Create tournament"
        self.questions["tournamentList"] = "2) Tournaments list"
        return self.questions
