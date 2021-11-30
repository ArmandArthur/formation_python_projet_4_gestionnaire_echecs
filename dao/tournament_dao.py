from dao.generique_dao import GeneriqueDao
from models.tournament_model import TournamentModel


class TournamentDao(GeneriqueDao):
    def __init__(self):
        super().__init__(TournamentModel)


tournament_dao = TournamentDao()
