class QuestionsRankPlayerView:
    def __init__(self):
        self.questions = {}

    def main(self):
        """
            Dict des questions sur le rank du joueur avec en clé l'attribut pydantic

            @return: Le dict
        """
        self.questions["id"] = "Player's ID :"
        self.questions["rank"] = "New rank :"
        return self.questions
