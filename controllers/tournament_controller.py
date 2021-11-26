from models.tournament_model import TournamentModel
from models.round_model import RoundModel
from models.match_model import MatchModel
from models.match_score_enum import MatchScoreEnum

from views.questions_tournament_view import QuestionsTournamentView
from views.formulaire_view import FormulaireView
from views.table_view import TableView
from controllers.player_controller import PlayerController

from dao.generique_dao import GeneriqueDao

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
        self.tournament_model = TournamentModel
        self.round_model = RoundModel
        self.match_model = MatchModel
        self.match_score_enum_model = MatchScoreEnum
        
        self.questions_tournament = QuestionsTournamentView().main()
        self.formulaire_view = FormulaireView()
        self.table_view = TableView()
        
        self.player_controller = PlayerController()

        self.generique_dao = GeneriqueDao(self.tournament_model)
        self.answers_tournament = {}

        self.points_players_dict = {}
        self.players_sort = []
        self.match_list_played = []
        
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
        return tournament

    def generate_round(self, tournament):
        if len(tournament.rounds) == 0:
            round_numero = str(1)
        else:
            round_numero = str(int(len(tournament.rounds))+1)

        round = self.round_model(
            name="ROUND "+round_numero,
            matchs= []
        )

        tournament.rounds.append(round)

        tournament_instance = self.generique_dao.update_item(tournament)
        self.generique_dao.save_item(tournament_instance.id)
        return tournament_instance

    def generate_first_round(self, tournament):
        players = tournament.players
        players_sort = []
        for id in players:
            players_sort.append(self.player_controller.generique_dao.items[int(id)])
            
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
            player_dao = self.player_controller.generique_dao.items[int(id)]
            self.players_sort.append(player_dao)
        
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
        tournament_instance = self.generique_dao.update_item(tournament)
        self.generique_dao.save_item(tournament_instance.id)
        
    def find_match(self, tournament_id):
        tournament = self.generique_dao.find_by_id(tournament_id)
        for key_round, round in enumerate(tournament.rounds):
            for key_match, match in enumerate(round.matchs):
                if match.score_first is None:
                    score = self.formulaire_view.display_match(match)
                    if(score == "q"):
                        return score
                    else:
                        score = self.match_score_enum_model(float(score))
                    tournament.rounds[key_round].matchs[key_match].score_first = score
                    tournament.rounds[key_round].date_end = datetime.today()
        tournament_instance = self.generique_dao.update_item(tournament)
        self.generique_dao.save_item(tournament_instance.id)
