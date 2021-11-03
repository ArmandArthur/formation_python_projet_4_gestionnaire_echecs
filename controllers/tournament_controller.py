#!/usr/bin/env python
# coding: utf-8


from models.tournament_model import TournamentModel
from views.questions_tournament_view import QuestionsTournamentView
from views.formulaire_view import FormulaireView

from dao.generique_dao import GeneriqueDao

from pydantic import ValidationError


class TournamentController:
    """
        Tournament Controller
    """
    def __init__(self):
        """
            Constructor, storage in attributs module and variables
        """
        self.tournament_model = TournamentModel
        self.questions_tournament = QuestionsTournamentView().main()
        self.formulaire_view = FormulaireView()
        self.generique_dao = GeneriqueDao('tournament')
        self.answers_tournament = {}

    def display_questions_tournament(self):
        self.formulaire_view.display_comments("create_tournament")
        answer = self.formulaire_view.display_questions(self.questions_tournament)
        self.answers_tournament = answer

        # New TOURNMAMENT
        return self.verify_tournament()

    def verify_tournament(self):
        newTounament = self.answers_tournament
        try:
            tournament = self.tournament_model(**newTounament)
            self.generique_dao.add(tournament)
            self.formulaire_view.display_comments("create_tournament_done")
            return True
        except ValidationError as e:
            errors = e.errors()
            self.formulaire_view.display_errors(errors)
            self.display_questions_tournament()
