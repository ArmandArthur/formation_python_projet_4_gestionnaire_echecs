from dao.generique_dao import GeneriqueDao
from models.player_model import PlayerModel


class PlayerDao(GeneriqueDao):
    def __init__(self):
        """
            Appelle le constructeur parent avec le model player
        """
        super().__init__(PlayerModel)


player_dao = PlayerDao()
