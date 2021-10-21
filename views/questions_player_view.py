#!/usr/bin/env python
# coding: utf-8

class QuestionsPlayerView:
    def __init__(self):
        self.questions = {}

    def main(self):
        self.questions['Name'] = 'What is your name?'
        self.questions['FirstName'] = 'What is your firstname?'
        self.questions['BirthdayDate'] = 'When were you born?'
        self.questions['Sexe'] = 'What is your sexe?'
        return self.questions
