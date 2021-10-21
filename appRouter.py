#!/usr/bin/env python
# coding: utf-8

from views.MenuPrincipalView import MenuPrincipalView
from views.MenuPrincipalPlayerView import MenuPrincipalPlayerView
from controllers.PlayerController import PlayerController

from pathlib import Path

class AppRouter:
    def __init__(self):
        self.MenuPrincipal = MenuPrincipalView()
        self.MenuPrincalPlayer = MenuPrincipalPlayerView()
        self.PlayerController = PlayerController
        self.main()
        
    def main(self):
        MenuPrincipalQuestions = self.MenuPrincipal.questionsMain()
        for question in MenuPrincipalQuestions.items():
            print(question)
        MenuPrincipalAnswer = input("Votre choix: ")
        print("\n")

        if(MenuPrincipalAnswer == "1"):
            MenuPrincipalPlayerQuestions = self.MenuPrincalPlayer.questionsPlayer()
            for question in MenuPrincipalPlayerQuestions.items():
                print(question)
            MenuPrincipalPlayerAnswer = input("Votre choix: ")
            print("\n")
           
            if(MenuPrincipalPlayerAnswer == "1"):
                self.PlayerController()

if __name__ == "__main__":
    AppRouter()