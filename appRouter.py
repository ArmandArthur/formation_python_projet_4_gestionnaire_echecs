#!/usr/bin/env python
# coding: utf-8

from views.menu_principal_view import MenuPrincipalView
from views.menu_principal_player_view import MenuPrincipalPlayerView
from views.main_view import MainView

from controllers.player_controller import PlayerController


class AppRouter:
    """
        CLASS ROUTER APP
    """
    def __init__(self):
        """
            STOCK VARIABLES ATTRIBUTS
        """
        self.menu_principal = MenuPrincipalView()
        self.menu_principal_player = MenuPrincipalPlayerView()
        self.player_controller = PlayerController

        self.main_view = MainView()

        self.questions = {}
        self.answer = None

        self.main()

    def main(self):
        self.questions = self.menu_principal.questions_main()
        self.answer = self.main_view.display_menu(self.questions)

        if(self.answer == "1"):
            self.questions = self.menu_principal_player.questions_player()
            self.answer = self.main_view.display_menu(self.questions)

            if(self.answer == "1"):
                self.player_controller()


if __name__ == "__main__":
    AppRouter()
