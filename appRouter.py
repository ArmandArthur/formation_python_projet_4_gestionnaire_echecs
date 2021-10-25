#!/usr/bin/env python
# coding: utf-8

from views.menu_principal_view import MenuPrincipalView
from views.menu_principal_player_view import MenuPrincipalPlayerView
from views.menu_sort_players_view import MenuSortPlayersView
from views.main_view import MainView
from views.table_view import TableView
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
        self.menu_sort_players = MenuSortPlayersView()
        self.player_controller = PlayerController()

        self.main_view = MainView()
        self.table_view = TableView()

        self.questions = {}
        self.answer = None

        self.main()

    def main(self):
        self.questions = self.menu_principal.questions_main()
        self.answer = self.main_view.display_menu(self.questions)

        if(self.answer == "1"):
            self.menu_player()

    def menu_sort(self):
        self.questions = self.menu_sort_players.sort_players()
        self.answer = self.main_view.display_menu(self.questions)
        if(self.answer != 'q'):
            list_players_sort = self.player_controller.sort_all_players(self.answer)
            self.table_view.display(list_players_sort)
            self.menu_sort()
        else:
            self.menu_player()

    def menu_player(self):
        self.questions = self.menu_principal_player.questions_player()
        self.answer = self.main_view.display_menu(self.questions)

        if(self.answer == "1"):
            self.menu_questions_player()
        elif(self.answer == "2"):
            self.menu_list_players()
        elif(self.answer == "q"):
            self.main()

    def menu_questions_player(self):
        is_create_player = self.player_controller.display_questions_player()
        if is_create_player is True:
            self.main()
    
    def menu_list_players(self):
        list_players = self.player_controller.display_all_players()
        self.table_view.display(list_players)
        self.menu_sort()
        
if __name__ == "__main__":
    AppRouter()
