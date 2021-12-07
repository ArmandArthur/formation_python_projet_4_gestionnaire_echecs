from models.round_model import RoundModel
from models.match_model import MatchModel
from models.match_score_enum import MatchScoreEnum

from views.questions_tournament_view import QuestionsTournamentView
from views.formulaire_view import FormulaireView
from views.table_view import TableView

from dao.player_dao import player_dao
from dao.tournament_dao import tournament_dao

from pydantic import ValidationError

from collections import defaultdict
from datetime import datetime


class TournamentController:
    """
        Tournament Controller
    """
    def __init__(self):
        """
            Constructor, storage in attributs module and variables
        """
        self.round_model = RoundModel
        self.match_model = MatchModel
        self.match_score_enum_model = MatchScoreEnum
        self.questions_tournament = QuestionsTournamentView().main()
        self.formulaire_view = FormulaireView()
        self.table_view = TableView()

        self.answers_tournament = {}

        self.points_players_dict = {}
        self.players_sort = []
        self.match_list_played = []
        self.iteration_match_key = 0

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
            try:
                player = player_dao.find_by_id(int(id))
                players_list.append(player.id)
            except AttributeError:
                self.formulaire_view.display_text('Invalid ID Player')
                self.display_questions_tournament()
                raise
        # New format datas
        newTounament['players'] = players_list
        # intension
        newTounament = {k: v for k, v in newTounament.items() if v}
        try:
            tournament_instance = tournament_dao.create_item(**newTounament)
            tournament_dao.save_item(tournament_instance.id)
            self.formulaire_view.display_comments("create_tournament_done")
            return True
        except ValidationError as e:
            errors = e.errors()
            self.formulaire_view.display_errors(errors)
            self.display_questions_tournament()

    def display_list_tournament(self):
        list_tournament = tournament_dao.all()

        self.table_view.display_tournaments_compact(list_tournament)
        tournament_id = self.formulaire_view.display_input()
        if(tournament_id == 'q'):
            return 'q'
        tournament = tournament_dao.find_by_id(int(tournament_id))
        return tournament

    def generate_round(self, tournament):
        if len(tournament.rounds) == 0:
            round_numero = str(1)
        else:
            round_numero = str(int(len(tournament.rounds))+1)

        round = self.round_model(
            name="ROUND "+round_numero,
            matchs=[]
        )

        tournament.rounds.append(round)

        # tournament_instance = tournament_dao.update_item(tournament)
        tournament_dao.save_item(tournament.id)
        return tournament

    def generate_first_round(self, tournament):
        players = tournament.players
        players_sort = []
        for id in players:
            player = player_dao.find_by_id(id)
            players_sort.append(player)

        players_sort = sorted(players_sort, key=lambda row: (-row.rank, row.name, row.firstname))
        # id à remplacer par rank

        group_first = players_sort[:len(players_sort)//2]
        group_second = players_sort[len(players_sort)//2:]

        match_list = []
        for p1, p2 in zip(group_first, group_second):
            match_list.append(self.match_model(
                player_id_first=p1.id,
                player_id_second=p2.id,
                score_first=None
            ))

        return match_list

    def generate_next_round(self, tournament):
        self.points_players_dict = self.points_players(tournament)
        self.matchs_played(tournament)

        players = tournament.players

        for id in players:
            player = player_dao.find_by_id(id)
            self.players_sort.append(player)

        self.players_sort = sorted(self.players_sort, key=lambda p: (-float(self.points_players_dict[p.id]), -p.rank))

        match_list = []

        while len(self.players_sort) > 0:
            p1 = self.players_sort.pop(0)
            p2 = self.search_game_next_round(p1, 0)
            match_list.append(self.match_model(
                player_id_first=p1.id,
                player_id_second=p2.id,
                score_first=None)
            )
        return match_list

    def search_game_next_round(self, player_1, iteration):
        player_2 = self.players_sort[iteration]
        new_game = (player_1, player_2)
        if new_game not in self.match_list_played:
            # Retire le joueur 2 de la liste
            self.players_sort.pop(iteration)
        else:
            iteration = iteration + 1
            self.search_game_next_round(player_1, iteration)
        return player_2

    def matchs_played(self, tournament):
        for round in tournament.rounds:
            # Permet de créer un round sans matchs
            if round.matchs is not None:
                for match in round.matchs:
                    game = (match.player_id_first, match.player_id_second)
                    self.match_list_played.append(game)

    def points_players(self, tournament):
        players = defaultdict(int)
        for round in tournament.rounds:
            # Permet de créer un round sans matchs
            if round.matchs is not None:
                for match in round.matchs:
                    if match.score_first is not None:
                        players[match.player_id_first] += float(match.score_first.value)
                    if match.score_second is not None:
                        players[match.player_id_second] += float(match.score_second.value)
        return players

    def generate_match(self, tournament, index_round):

        if index_round == 0:
            match_list = self.generate_first_round(tournament)
        else:
            match_list = self.generate_next_round(tournament)

        tournament.rounds[index_round].matchs = match_list
        # tournament_instance = tournament_dao.update_item(tournament)
        tournament_dao.save_item(tournament.id)

    def save_matchs(self, tournament, key_round):
        tournament.rounds[key_round].date_end = datetime.today()
        # tournament_instance = tournament_dao.update_item(tournament)
        tournament_dao.save_item(tournament.id)

    def find_match(self, tournament_params, key_round, key_match, match):
        return self.find_match_current(tournament_params, key_round, key_match, match)

    def find_match_current(self, tournament, key_round, key_match, match):
        self.formulaire_view.display_text(tournament.rounds[key_round].name+' / MATCH '+str(key_match+1))
        score = self.formulaire_view.display_match(match)
        if score == "q":
            return score
        else:
            enum_list_match_score = {k: v.value for k, v in enumerate(self.match_score_enum_model)}
            try:
                score = float(score)
            except ValueError:
                self.formulaire_view.display_text("Score is not a float")
                return self.find_match_current(tournament, key_round, key_match, match)
            if score in enum_list_match_score.values():
                score = self.match_score_enum_model(score)
                tournament.rounds[key_round].matchs[key_match].score_first = score
                return tournament
            else:
                return self.find_match_current(tournament, key_round, key_match, match)
