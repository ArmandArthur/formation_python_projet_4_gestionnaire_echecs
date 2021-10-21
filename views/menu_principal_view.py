#!/usr/bin/env python
# coding: utf-8

class MenuPrincipalView:
    def __init__(self):
        self.questions = {}

    def questions_main(self):
        self.questions["player"] = "1) Mode player"
        self.questions["tournament"] = "2) Mode tournament"
        return self.questions
