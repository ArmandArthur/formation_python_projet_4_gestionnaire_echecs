from models.player_model import PlayerModel
from views.questions_player_view import QuestionsPlayerView
from views.questions_rank_player_view import QuestionsRankPlayerView
from views.formulaire_view import FormulaireView

from dao.player_dao import player_dao

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
        self.questions_rank_player = QuestionsRankPlayerView().main()
        self.formulaire_view = FormulaireView()
        self.answers_player = {}
        self.answers_rank_player = {}

    def display_questions_player(self):
        self.formulaire_view.display_comments("create_player")
        answer = self.formulaire_view.display_questions(self.questions_player)
        self.answers_player = answer
        # New PLAYER
        return self.verify_player()

    def display_questions_rank_player(self):
        self.formulaire_view.display_comments("edit_rank_player")
        answer = self.formulaire_view.display_questions(self.questions_rank_player)
        self.answers_rank_player = answer
        # New PLAYER
        return self.verify_rank_player()

    def verify_player(self):
        newPlayer = self.answers_player
        try:
            player_instance = player_dao.create_item(**newPlayer)
            player_dao.save_item(player_instance.id)
            self.formulaire_view.display_comments("create_player_done")
        except ValidationError as e:
            errors = e.errors()
            self.formulaire_view.display_errors(errors)

    def verify_rank_player(self):
        edit_player = self.answers_rank_player
        try:
            try:
                edit_player_id = int(edit_player['id'])
            except ValueError:
                return None
            player_instance = player_dao.find_by_id(edit_player_id)
            try:
                player_instance.rank = edit_player['rank']
                player_dao.save_item(player_instance.id)
                self.formulaire_view.display_comments("edit_rank_player_done")
            except ValidationError as e:
                errors = e.errors()
                self.formulaire_view.display_errors(errors)
        except KeyError:
            self.formulaire_view.display_key_error()

    def display_all_players(self):
        list_players = player_dao.all()
        players_sort = sorted(list_players, key=lambda row: (row.id))
        return players_sort

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
