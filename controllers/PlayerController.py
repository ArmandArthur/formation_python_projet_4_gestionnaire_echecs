#!/usr/bin/env python
# coding: utf-8


from models.Player import PlayerModel
from views.QuestionsPlayerView import QuestionsPlayerView
from views.formulaire_view import FormulaireView

from pydantic import ValidationError

import json

class PlayerController:
    """
        DOC
    """
    def __init__(self):
        self.modelPlayer = PlayerModel
        self.questionsPlayer = QuestionsPlayerView().main()
        self.FormulaireView = FormulaireView()
        self.answersPlayer = {}
        self.pathPlayer = 'datas/players/'
        self.menu()
        
    def menu(self):

        self.QuestionsPlayer()

    def QuestionsPlayer(self):
        self.FormulaireView.display_comments("create_player")
        self.answersPlayer = self.FormulaireView.display_questions(self.questionsPlayer)

        # New PLAYER
        self.VerifyPlayer()

    def VerifyPlayer(self):
        newPlayer = self.answersPlayer
        try:
            player = self.modelPlayer(**newPlayer)

        except ValidationError as e:
            errors = e.errors()
            self.FormulaireView.display_errors(errors)
            self.QuestionsPlayer()

    # def InsertJsonPlayer(self, player):
    #     """
    #         DOC
    #     """
    #     dictPlayer = player.dict()

    #     # default STR for date
    #     # ensure ascii allow accents
    #     jsonPlayerWithIndent = json.dumps(dictPlayer, indent=4, sort_keys=True, default=str, ensure_ascii=False)
        
    #     # Remove accent
    #     nameFile = self.strip_accents(player.Name+'_'+player.FirstName)

    #     # Create FOLDER
    #     Path(self.pathPlayer).mkdir(parents=True, exist_ok=True)

    #     #Create FILE
    #     with open(self.pathPlayer+nameFile+".json", "w") as outfile:
    #         outfile.write(jsonPlayerWithIndent)

    # def strip_accents(self, text):
    #     try:
    #         text = unicode(text, 'utf-8')
    #     except (TypeError, NameError): # unicode is a default on python 3 
    #         pass
    #     text = unicodedata.normalize('NFD', text)
    #     text = text.encode('ascii', 'ignore')
    #     text = text.decode("utf-8")
    #     return str(text)
