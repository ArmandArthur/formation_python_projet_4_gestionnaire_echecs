from dao.generique_dao import GeneriqueDao
from models.tournament_model import TournamentModel


class TournamentDao(GeneriqueDao):
    def __init__(self):
        """
            Appelle le constructeur parent avec le model tournament
        """
        super().__init__(TournamentModel)


tournament_dao = TournamentDao()
