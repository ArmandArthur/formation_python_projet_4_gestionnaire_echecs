#!/usr/bin/env python
# coding: utf-8

class MenuPrincipalPlayerView:
    def __init__(self):
        self.questions = {}
        
    def questionsPlayer(self):
        self.questions["playerCreate"] = "1) Create player"
        self.questions["playerList"] = "2) Players list" 
        return self.questions
