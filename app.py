#!/usr/bin/env python
# coding: utf-8


from controllers.Player import PlayerController

from views.QuestionsPlayerView import QuestionsPlayerView

class App:
    def __init__(self, controllerPlayer, QuestionsPlayer):
        self.controllerPlayer = controllerPlayer
        self.arthurPlayer = {'Id': 1, 'Name': 'ARMAND', 'FirstName': 'Arthur', 'BirthdayDate': '1986-08-29 00:00:00', 'Sexe': 'H', 'Classement' : '1'}
        self.questionsPlayer = QuestionsPlayerView().main()
        self.answersPlayer = {}
        self.main()
        
    def main(self):
        player = self.controllerPlayer(**self.arthurPlayer)
        self.defQuestionsPlayer()

    def defQuestionsPlayer(self):
        for key, question in self.questionsPlayer.items():
            self.answersPlayer[key] = input(question)
        print(self.answersPlayer)
        
if __name__ == "__main__":
    App(
        PlayerController,
        QuestionsPlayerView
    )