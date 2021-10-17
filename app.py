#!/usr/bin/env python
# coding: utf-8


from controllers.Player import PlayerController

from views.QuestionsPlayerView import QuestionsPlayerView

class App:
    def __init__(self, controllerPlayer, QuestionsPlayer):
        self.controllerPlayer = controllerPlayer
        self.questionsPlayer = QuestionsPlayerView().main()
        self.answersPlayer = {}
        self.main()
        
    def main(self):

        self.defQuestionsPlayer()

    def defQuestionsPlayer(self):
        for key, question in self.questionsPlayer.items():
            self.answersPlayer[key] = input(question)
        # New PLAYER
        newPlayer = self.answersPlayer
        player = self.controllerPlayer(**newPlayer)
        print(player)
        
if __name__ == "__main__":
    App(
        PlayerController,
        QuestionsPlayerView
    )