from .main_view import MainView
from datetime import datetime, date
from dao.player_dao import player_dao


class TableView(MainView):
    def display(self, datas):
        """
            Affiche la liste des joueurs

            @param: datas => liste d'instance pydantic
        """
        if(len(datas) > 0):
            datas_keys = datas[0].__fields__.keys()
            row_format = "{:<20}" * (len(datas_keys))
            print(row_format.format(*datas_keys))
            for data in datas:
                list_values = list(data.dict().values())
                list_values_format = []
                for i in list_values:
                    if i is None:
                        list_values_format.append("None")
                    elif isinstance(i, date):
                        DATETIME_FORMAT = '%Y-%m-%d'
                        list_values_format.append(datetime.strftime(i, DATETIME_FORMAT))
                    else:
                        list_values_format.append(i)
                print(row_format.format(*list_values_format))
        else:
            print("No player create...")

    def display_tournaments_compact(self, list_tournament):
        """
            Affiche la liste des tournoi en mode simplifié

            @param: list_tournament => liste d'instance pydantic
        """
        row_format = "{:<20}" * 2
        headers = ['id', 'name']
        print(row_format.format(*headers))
        for tournament in list_tournament:
            list_values_format = []
            for _key, i in tournament:
                if _key == 'id' or _key == 'name':
                    list_values_format.append(i)
            print(row_format.format(*list_values_format))

    def display_rapport(self, tournament):
        """
            Affiche un rapport du tournoi

            @param: tournament => instance pydantic
        """
        print("Tournament name : "+tournament.name)
        print("\n")
        for round in tournament.rounds:
            print(round.name)
            for index_match, match in enumerate(round.matchs):
                player_1 = player_dao.find_by_id(match.player_id_first)
                player_2 = player_dao.find_by_id(match.player_id_second)
                print("     Match "+str(index_match+1))
                if match.score_first is not None:
                    print("          "+player_1.firstname+" "+player_1.name+" ("+str(match.score_first.value)+")")
                    print("          "+player_2.firstname+" "+player_2.name+" ("+str(match.score_second.value)+")")
            print("\n")
