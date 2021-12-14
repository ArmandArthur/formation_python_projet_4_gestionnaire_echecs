#!/usr/bin/env python
# coding: utf-8

class MenuPrincipalPlayerView:
    def __init__(self):
        self.questions = {}

    def questions_player(self):
        """
            Dict des questions du menu joueur

            @return: Le dict
        """
        self.questions["playerCreate"] = "1) Create player"
        self.questions["playerList"] = "2) Players list"
        self.questions["playerRank"] = "3) Edit rank's player"
        return self.questions
