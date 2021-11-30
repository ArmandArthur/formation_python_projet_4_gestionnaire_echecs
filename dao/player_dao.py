from dao.generique_dao import GeneriqueDao
from models.player_model import PlayerModel


class PlayerDao(GeneriqueDao):
    def __init__(self):
        super().__init__(PlayerModel)


player_dao = PlayerDao()
