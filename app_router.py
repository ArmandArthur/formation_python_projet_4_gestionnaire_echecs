#!/usr/bin/env python
# coding: utf-8

from views.menu_principal_view import MenuPrincipalView
from views.menu_principal_player_view import MenuPrincipalPlayerView
from views.menu_principal_tournament_view import MenuPrincipalTournamentView

from views.menu_sort_players_view import MenuSortPlayersView

from views.main_view import MainView
from views.table_view import TableView

from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController


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
        self.menu_principal_tournament = MenuPrincipalTournamentView()

        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController()

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
        elif(self.answer == "2"):
            self.menu_tournament()

    # MENU PLAYER
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
        elif(self.answer == "3"):
            self.menu_list_players_edit()
        elif(self.answer == "q"):
            self.main()

    def menu_list_players_edit(self):
        list_players = self.player_controller.display_all_players()
        self.table_view.display(list_players)
        self.menu_questions_rank_player()

    def menu_questions_rank_player(self):
        self.player_controller.display_questions_rank_player()
        self.main()

    def menu_questions_player(self):
        self.player_controller.display_questions_player()
        self.main()

    def menu_list_players(self):
        list_players = self.player_controller.display_all_players()
        self.table_view.display(list_players)
        self.menu_sort()

    # MENU TOUNRMAMET
    def menu_tournament(self):
        self.questions = self.menu_principal_tournament.questions_tournament()
        self.answer = self.main_view.display_menu(self.questions)

        if(self.answer == "1"):
            self.menu_questions_tournament()
        elif(self.answer == "2"):
            self.menu_start_tournament()
        elif(self.answer == "q"):
            self.main()

    def menu_questions_tournament(self):
        self.tournament_controller.display_questions_tournament()
        self.main()

    def menu_start_tournament(self):
        tournament = self.tournament_controller.display_list_tournament()
        1.0
        if(tournament == 'q'):
            self.menu_tournament()
        while len(tournament.rounds) < tournament.rounds_number:
            tournament = self.tournament_controller.generate_round(tournament)

        for index, round in enumerate(tournament.rounds):
            if round.date_end is None:
                if len(round.matchs) == 0:
                    self.tournament_controller.generate_match(tournament, index)
                for key_match, match in enumerate(tournament.rounds[index].matchs):
                    tounrnament_return = self.tournament_controller.find_match(tournament, index, key_match, match)
                    if tounrnament_return == 'q':
                        self.menu_tournament()
                self.tournament_controller.save_matchs(tounrnament_return, index)
        if len(tournament.rounds) == tournament.rounds_number:
            self.main_view.display_comments('finish_tournament')
            self.main()


if __name__ == "__main__":
    AppRouter()
