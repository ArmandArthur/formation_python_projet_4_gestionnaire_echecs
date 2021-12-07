#!/usr/bin/env python
# coding: utf-8

class MainView:
    def __init__(self):
        self.questions = {}

    def display_menu(self, questions):
        self.questions = questions
        for _, question in self.questions.items():
            print(question)
        answer = input("Your choice: ")
        print("\n")
        return answer

    def display_comments(self, string):
        if(string == 'create_player'):
            print("### Menu : Create Player ###")
        elif(string == 'create_player_done'):
            print("### Player create ###")
        elif(string == 'create_tournament'):
            print("### Menu : Create Tournament ###")
        elif(string == 'finish_tournament'):
            print("### Menu : Tournament finished ###")
        elif(string == 'edit_rank_player'):
            print("### Player edition rank ###")
        elif(string == 'edit_rank_player_done'):
            print("### Rank is edited ###")
            
        print("\n")

    def display_errors(self, errors):
        print("\n")
        for error_item in errors:
            print("The field "+error_item["loc"][0]+" is invalid")
            print("Message error: "+error_item["msg"])
            print("\n")
            
    def display_key_error(self, e):
        print("\n")
        print("Invalid Id")
        print("\n")
            
    def display_input(self):
        answer = input("Your choice (id tournament): ")
        print("\n")
        return answer

    def display_text(self, text):
        print("\n")
        print('*** '+text+' ***')
