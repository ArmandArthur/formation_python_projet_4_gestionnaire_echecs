#!/usr/bin/env python
# coding: utf-8

class QuestionsTournamentView:
    def __init__(self):
        self.questions = {}

    def main(self):
        """
            Dict des questions sur le tournoi avec en clé l'attribut pydantic

            @return: Le dict
        """
        self.questions['name'] = 'What is the name about tournament?'
        self.questions['place'] = 'What is the tournament place?'
        self.questions['start_date'] = 'When is the beginning?'
        self.questions['end_date'] = 'When is the the end?'
        self.questions['rounds_number'] = 'Number of rounds (4 default)'
        self.questions['players'] = 'Who plays? Ex: id1,id2,id3 etc..'
        return self.questions
