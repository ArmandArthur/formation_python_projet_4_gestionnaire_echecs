#!/usr/bin/env python
# coding: utf-8

from views.MenuPrincipalView import MenuPrincipalView
from views.MenuPrincipalPlayerView import MenuPrincipalPlayerView
from views.main_view import MainView

from controllers.PlayerController import PlayerController

class AppRouter:
    def __init__(self):

        self.MenuPrincipal = MenuPrincipalView()
        self.MenuPrincalPlayer = MenuPrincipalPlayerView()
        self.PlayerController = PlayerController

        self.MainView = MainView()

        self.questions = {}
        self.answer = None
        
        self.main()
        
    def main(self):
        self.questions = self.MenuPrincipal.questionsMain()
        self.answer = self.MainView.display_menu(self.questions)

        if(self.answer == "1"):
            self.questions = self.MenuPrincalPlayer.questionsPlayer()
            self.answer = self.MainView.display_menu(self.questions)
           
            if(self.answer == "1"):
                self.PlayerController()

if __name__ == "__main__":
    AppRouter()