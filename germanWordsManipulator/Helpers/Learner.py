from State import State


class Learner:
    @staticmethod
    def learnWords(quantity=30):
        words = State.getEntity("words").getWordsToLearn(quantity)
        phrases = State.getEntity("phrases").getPhrasesToLearn(max(1, int(quantity / 3)))

        print(2)
