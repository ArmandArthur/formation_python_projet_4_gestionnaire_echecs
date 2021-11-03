#!/usr/bin/env python
# coding: utf-8

class QuestionsTournamentView:
    def __init__(self):
        self.questions = {}

    def main(self):
        self.questions['Name'] = 'What is the name about tournament?'
        self.questions['Place'] = 'What is the tournament place?'
        self.questions['StartDate'] = 'When is the beginning?'
        self.questions['EndDate'] = 'When is the the end?'
        self.questions['RoundsNumber'] = 'Number of rounds (4 default)'
        return self.questions
