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

    def update(self, wordsData):
        for i in range(0, len(wordsData), self._step):
            data, frequencies = {}, {}
            # Save data in batches in order to avoid losing the whole progress in case of an error
            for j in range(i, min(i + self._step, len(wordsData)), 1):
                word = wordsData[j]

                data[word["lemma"]] = dict({
                    **({"word_translation": word["translation"]} if "translation" in word else {}),
                    "word_is_learn_taken": True
                })

            super().update(list(data.values()))