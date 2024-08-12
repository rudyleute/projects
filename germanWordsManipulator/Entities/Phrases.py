from .Words import Words
from State import State


class Phrases(Words):
    def __init__(self):
        self.__phrasesCode = State.getEntity("speechParts").getPhrasesCode()
        super().__init__()

    def add(self, wordsData, isLearnTaken=False, isArticleTaken=False):
        for word in wordsData:
            word["speechPart"] = self.__phrasesCode

        super().add(wordsData, frequency=False, isLearnTaken=isLearnTaken, isArticleTaken=isArticleTaken)

    def addBaseLangData(self, wordsData, isTaken=False):
        for word in wordsData:
            word["speechPart"] = self.__phrasesCode

        super().addBaseLangData(wordsData, isTaken)
