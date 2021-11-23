from .main_view import MainView


class FormulaireView(MainView):
    def __init__(self):
        self.items = {}
        self.items_answer = {}

    def display_questions(self, items):
        self.items = items
        for key, question in self.items.items():
            self.items_answer[key] = input(question)
        print("\n")
        return self.items_answer

    def display_match(self, match):
        print(match.player_id_first)
        print(match.player_id_second)

        score = input("First player score (Values allowed: 1.0, 0.5, 0.0):")
        return score