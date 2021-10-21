#!/usr/bin/env python
# coding: utf-8

from views.MenuPrincipalView import MenuPrincipalView
from views.MenuPrincipalPlayerView import MenuPrincipalPlayerView

from controllers.PlayerController import PlayerController

class AppRouter:
    def __init__(self):
        self.MenuPrincipal = MenuPrincipalView()
        self.MenuPrincalPlayer = MenuPrincipalPlayerView()
        self.PlayerController = PlayerController

        self.questions = {}
        self.answer = None
        
        self.main()
        
    def main(self):
        self.questions = self.MenuPrincipal.questionsMain()
        self.displayMenu()

        if(self.answer == "1"):
            self.questions = self.MenuPrincalPlayer.questionsPlayer()
            self.displayMenu()
           
            if(self.answer == "1"):
                self.PlayerController()

    def displayMenu(self):
        for key, question in self.questions.items():
            print(question)
        self.answer = input("Votre choix: ")
        print("\n")

if __name__ == "__main__":
    AppRouter()