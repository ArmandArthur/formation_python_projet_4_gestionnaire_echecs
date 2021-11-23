#!/usr/bin/env python
# coding: utf-8


from posixpath import split
from models.player_model import PlayerModel
from views.questions_player_view import QuestionsPlayerView
from views.formulaire_view import FormulaireView

from dao.generique_dao import GeneriqueDao

from pydantic import ValidationError


class PlayerController:
    """
        Controller Player
    """
    def __init__(self):
        """
            Constructor, storage in attributs module and variables
        """
        self.player_model = PlayerModel
        self.questions_player = QuestionsPlayerView().main()
        self.formulaire_view = FormulaireView()
        self.generique_dao = GeneriqueDao(self.player_model)
        self.answers_player = {}

    def display_questions_player(self):
        self.formulaire_view.display_comments("create_player")
        answer = self.formulaire_view.display_questions(self.questions_player)
        self.answers_player = answer
        # New PLAYER
        return self.verify_player()

    def verify_player(self):
        newPlayer = self.answers_player
        try:
            player_instance = self.generique_dao.create_item(**newPlayer)
            self.generique_dao.save_item(player_instance.id)
            self.formulaire_view.display_comments("create_player_done")
        except ValidationError as e:
            errors = e.errors()
            self.formulaire_view.display_errors(errors)
            input("Impossible to create player")
    
    def display_all_players(self):
        list_players = self.generique_dao.all()
        return list_players
    
    def sort_all_players(self, answers_keys):
        self.answers_keys_sort = answers_keys

        players = self.display_all_players()
        players_sort = sorted(players, key=lambda row: self.sort_tuple(row))
        return players_sort
    
    def sort_tuple(self, row):
        # Split answer
        split_keys_sort = self.answers_keys_sort.split(',')
        tuple_sort = ()

        # Verify if colonne exist
        player_model_attributs = list(self.player_model.__fields__.keys())
        
        # Create tuple with values answers
        for attribut_player in split_keys_sort:
            if attribut_player in player_model_attributs:
                tuple_sort = tuple_sort + (getattr(row, attribut_player), )
        return tuple_sort