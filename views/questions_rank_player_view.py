class QuestionsRankPlayerView:
    def __init__(self):
        self.questions = {}

    def main(self):
        self.questions["id"] = "Player's ID :"
        self.questions["rank"] = "New rank :"
        return self.questions
