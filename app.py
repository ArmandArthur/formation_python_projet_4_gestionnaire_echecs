#!/usr/bin/env python
# coding: utf-8


from models.Player import PlayerModel
from views.QuestionsPlayerView import QuestionsPlayerView

from pydantic import ValidationError

import json
import unicodedata
from pathlib import Path

class App:
    def __init__(self):
        self.modelPlayer = PlayerModel
        self.questionsPlayer = QuestionsPlayerView().main()
        self.answersPlayer = {}
        self.pathPlayer = 'datas/players/'
        self.main()
        
    def main(self):

        self.QuestionsPlayer()

    def QuestionsPlayer(self):
        for key, question in self.questionsPlayer.items():
            self.answersPlayer[key] = input(question)
        
        # New PLAYER
        self.VerifyPlayer()

    def VerifyPlayer(self):
        newPlayer = self.answersPlayer
        try:
            player = self.modelPlayer(**newPlayer)
            self.InsertJsonPlayer(player)
        except ValidationError as e:
            print(e.json())

    def InsertJsonPlayer(self, player):
        dictPlayer = player.dict()

        # default STR for date
        # ensure ascii allow accents
        jsonPlayerWithIndent = json.dumps(dictPlayer, indent=4, sort_keys=True, default=str, ensure_ascii=False)
        
        # Remove accent
        nameFile = self.strip_accents(player.Name+'_'+player.FirstName)

        # Create FOLDER
        Path(self.pathPlayer).mkdir(parents=True, exist_ok=True)

        #Create FILE
        with open(self.pathPlayer+nameFile+".json", "w") as outfile:
            outfile.write(jsonPlayerWithIndent)

    def strip_accents(self, text):
        try:
            text = unicode(text, 'utf-8')
        except (TypeError, NameError): # unicode is a default on python 3 
            pass
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
        return str(text)

if __name__ == "__main__":
    App()