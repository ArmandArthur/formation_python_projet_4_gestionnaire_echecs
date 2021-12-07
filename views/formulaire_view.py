from .main_view import MainView
from dao.generique_dao import GeneriqueDao
from models.player_model import PlayerModel


class FormulaireView(MainView):
    def __init__(self):
        self.items = {}
        self.items_answer = {}
        self.dao_players = None

    def display_questions(self, items):
        self.items = items
        for key, question in self.items.items():
            self.items_answer[key] = input(question)
        print("\n")
        return self.items_answer

    def display_match(self, match):
        self.dao_players = GeneriqueDao(PlayerModel)
        player_1 = self.dao_players.find_by_id(match.player_id_first)
        player_2 = self.dao_players.find_by_id(match.player_id_second)
        print(str(match.player_id_first)+' ('+player_1.name+' '+player_1.firstname+')')
        print(str(match.player_id_second)+' ('+player_2.name+' '+player_2.firstname+')')

        score = input("First player score (Values allowed: 1.0, 0.5, 0.0):")
        return score
