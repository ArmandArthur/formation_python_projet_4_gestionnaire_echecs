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
            Déclarations des variables de classe principales
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
        """
            Affiche les questions de la création d'un tournoi

            @return: instance de tournament pydantic
        """
        self.formulaire_view.display_comments("create_tournament")
        answer = self.formulaire_view.display_questions(self.questions_tournament)
        self.answers_tournament = answer

        # New TOURNMAMENT
        return self.verify_tournament()

    def verify_tournament(self):
        """
            Vérifie si les joueurs saisies sont bien dans le DAO player
            + création du tounoi avec validation pydantic + erreurs

            @return: instance de tournament pydantic
        """
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

    def display_rapport_tournament(self, tournament):
        """
            Appelle la vue des rapports

            @param: tournament model
        """
        self.table_view.display_rapport(tournament)

    def display_list_tournament(self):
        """
            Affiche la liste des tournois

            @param: q (quitter) ou error
        """
        list_tournament = tournament_dao.all()

        self.table_view.display_tournaments_compact(list_tournament)
        tournament_id = self.formulaire_view.display_input()
        if(tournament_id == 'q'):
            return 'q'
        try:
            tournament_id = int(tournament_id)
        except ValueError as e:
            self.formulaire_view.display_error_simple(e)
            return 'error'
        try:
            tournament = tournament_dao.find_by_id(tournament_id)
            return tournament
        except KeyError:
            self.formulaire_view.display_key_error()
            return 'error'

    def generate_round(self, tournament):
        """
            Génération des rounds avec leur nom

            @param: tournament
            @return: tournament
        """
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
        """
            Génération le 1er round en fonction du rank, name, firstname

            @param: tournament
            @return: liste of match pydantic
        """
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
        """
            Génération des rounds suivant en fonction des points des joueurs dans le tournoi

            @param: tournament
            @return: liste of match pydantic
        """
        self.points_players_dict = self.points_players(tournament)
        self.matchs_played(tournament)

        players = tournament.players

        self.players_sort = []
        for id in players:
            player = player_dao.find_by_id(id)
            self.players_sort.append(player)

        self.players_sort = sorted(self.players_sort, key=lambda p: (-float(self.points_players_dict[p.id]), -p.rank))

        match_list = []

        while len(self.players_sort) > 1:
            p1 = self.players_sort.pop(0)
            p2 = self.search_game_next_round(p1, 0)
            match_list.append(self.match_model(
                player_id_first=p1.id,
                player_id_second=p2.id,
                score_first=None)
            )
        return match_list

    def search_game_next_round(self, player_1, iteration):
        """
            Cherche un nouveau adversaire au joueur_1 si il a déjà joué le joueur 2
            + supprime le joueur 2 de la liste si validé.

            @param: player_1 : player instance
            @param: iteration : l'iteration pour trouver le suivant
            @return: recursive fonction
        """
        player_2 = self.players_sort[iteration]
        new_game = (player_1.id, player_2.id)
        if new_game in self.match_list_played:
            # sinon bug 0.5 4ème round
            if len(self.players_sort) > 1:
                iteration = iteration + 1
                return self.search_game_next_round(player_1, iteration)
        else:
            self.players_sort = [i for i in self.players_sort if not (i.id == player_2.id)]
        return player_2

    def matchs_played(self, tournament):
        """
            Ajoute les matchs joués dans une liste.

            @param: tournament
        """
        for round in tournament.rounds:
            # Permet de créer un round sans matchs
            if round.matchs is not None:
                for match in round.matchs:
                    game = (match.player_id_first, match.player_id_second)
                    self.match_list_played.append(game)

    def points_players(self, tournament):
        """
            Calcul le nombre de points des joueurs au total dans le tournoi

            @param: tournament
            @return: dictionnaire des points en fonction de l'id du joueur
        """
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
        """
            Génération des matchs

            @param: tournament
            @param2: l'index du round
        """
        if index_round == 0:
            match_list = self.generate_first_round(tournament)
        else:
            match_list = self.generate_next_round(tournament)

        tournament.rounds[index_round].matchs = match_list
        # tournament_instance = tournament_dao.update_item(tournament)
        tournament_dao.save_item(tournament.id)

    def save_matchs(self, tournament, key_round):
        """
            Met à jour la date de fin du round sur la date actuelle

            @param: tournament
            @param2: l'index du round
        """
        tournament.rounds[key_round].date_end = datetime.today()
        # tournament_instance = tournament_dao.update_item(tournament)
        tournament_dao.save_item(tournament.id)

    def find_match(self, tournament_params, key_round, key_match, match):
        """
            Cherche un match

            @param: tournament_params
            @param2: l'index du round
            @param3: l'index du match
            @param4: le match
            @return: la fonction find_match_current
        """
        return self.find_match_current(tournament_params, key_round, key_match, match)

    def find_match_current(self, tournament, key_round, key_match, match):
        """
            Fonction récursive qui relance la saisie du match si invalide saisie

            @param: tournament_params
            @param2: l'index du round
            @param3: l'index du match
            @param4: le match
            @return: tournament / quitter ou elle même si erreur
            @raise: score non valide
        """
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
