#!/usr/bin/env python
# coding: utf-8


from models.tournament_model import TournamentModel
from views.questions_tournament_view import QuestionsTournamentView
from views.formulaire_view import FormulaireView
from views.table_view import TableView
from controllers.player_controller import PlayerController

from dao.generique_dao import GeneriqueDao

from pydantic import ValidationError


class TournamentController:
    """
        Tournament Controller
    """
    def __init__(self):
        """
            Constructor, storage in attributs module and variables
        """
        self.tournament_model = TournamentModel
        self.questions_tournament = QuestionsTournamentView().main()
        self.formulaire_view = FormulaireView()
        self.table_view = TableView()
        
        self.player_controller = PlayerController()

        self.generique_dao = GeneriqueDao(self.tournament_model)
        self.answers_tournament = {}

    def display_questions_tournament(self):
        self.formulaire_view.display_comments("create_tournament")
        answer = self.formulaire_view.display_questions(self.questions_tournament)
        self.answers_tournament = answer

        # New TOURNMAMENT
        return self.verify_tournament()

    def verify_tournament(self):
        newTounament = self.answers_tournament
        
        players_id_list = newTounament['players'].split(',')
        players_list = []
        for id in players_id_list:
            players_list.append(int(id))
    
        # New format datas
        newTounament['players'] = players_list
        
        # intension 
        newTounament = {k: v for k, v in newTounament.items() if v}
        
        try:
            tournament_instance = self.generique_dao.create_item(**newTounament)
            self.generique_dao.save_item(tournament_instance.id)
            self.formulaire_view.display_comments("create_tournament_done")
            return True
        except ValidationError as e:
            errors = e.errors()
            self.formulaire_view.display_errors(errors)
            self.display_questions_tournament()

    def display_list_tournament(self):
        list_tournament = self.generique_dao.all()
        self.table_view.display_tournaments_compact(list_tournament)
        tournament_id = self.formulaire_view.display_input()
        tournament = self.generique_dao.items[int(tournament_id)]
        
        round = []
        matchs = self.generate_matching(tournament)
        
        # for match in matchs:
        #     round.append(match)
        # match = []
        # match['player_id_first'] = id1
        # match['player_id_second'] = id2
        
    def generate_matching(self, tournament):
        players = tournament.players
        players_sort = []
        for id in players:
            players_sort.append(self.player_controller.generique_dao.items[int(id)])
            
        players_sort = sorted(players_sort, key=lambda row: (row.rank, row.name, row.firstname))
        
        group_first = players_sort[:len(players_sort)//2]
        print(group_first)
        group_second = players_sort[len(players_sort)//2:]
        print(group_second)
        