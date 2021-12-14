#!/usr/bin/env python
# coding: utf-8

class QuestionsPlayerView:
    def __init__(self):
        self.questions = {}

    def main(self):
        """
            Dict des questions sur le joueur avec en clé l'attribut pydantic

            @return: Le dict
        """
        self.questions['name'] = 'What is your name?'
        self.questions['firstname'] = 'What is your firstname?'
        self.questions['birthday_date'] = 'When were you born?'
        self.questions['sexe'] = 'What is your sexe?'
        self.questions['rank'] = 'Rank?'
        return self.questions
