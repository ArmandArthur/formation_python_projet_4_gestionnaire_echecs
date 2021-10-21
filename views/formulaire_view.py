#!/usr/bin/env python
# coding: utf-8
from .main_view import MainView


class FormulaireView(MainView):
    def __init__(self):
        self.items = {}
        self.items_answer = {}

    def display_questions(self, items):
        self.items = items
        for key, question in self.items.items():
            self.items_answer[key] = input(question)
        print("\n")
        return self.items_answer
