#!/usr/bin/env python
# coding: utf-8

class MainView:
    def __init__(self):
        self.questions = {}

    def display_menu(self, questions):
        self.questions = questions
        for _, question in self.questions.items():
            print(question)
        answer = input("Your chooce: ")
        print("\n")
        return answer

    def display_comments(self, string):
        if(string == 'create_player'):
            print("### Menu : Create Player ###")
        elif(string == 'create_player_done'):
            print("### Player create ###")
        elif(string == 'create_tournament'):
            print("### Menu : Create Tournament ###")

    def display_errors(self, errors):
        for error_item in errors:
            print("The field "+error_item["loc"][0]+" is invalid")
            print("Message error: "+error_item["msg"])
            print("\n")

