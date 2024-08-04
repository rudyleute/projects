from .Tables import Tables
from Helpers.Requests import Requests
from Helpers.Corpus import Corpus
from State import State
from collections import defaultdict


class Words(Tables):
    def __init__(self):
        super().__init__("word")

    def __getList(self, keys, params=None):
        if params is None:
            params = dict()
        params["select"] = set(keys)

        return self.get(params, isDict=False)

    def getWordsList(self, params=None):
        return self.__getList({'word_lemma'}, params)

    def getTranslationsList(self, params=None):
        return self.__getList({'word_translation'}, params)

    def addBaseLangData(self, wordsData, isTaken=False):
        speechParts = State.getEntity("speechParts").get()
        step = 10
        for i in range(0, len(wordsData), step):
            data, frequencies = {}, {}
            # Save data in batches in order to avoid losing the whole progress in case of an error
            for j in range(i, min(i + step, len(wordsData)), 1):
                word = wordsData[j]

                # TODO figure out how to process phrases from the aforementioned file (can contain 2+ words as it
                #  turns out)
                data[word["lemma"]] = dict({
                    "word_translation": word["word"],
                    "word_fk_speech_part_id": speechParts[word["speechPart"]]["uuid"],
                    "word_is_learn_taken": isTaken
                })

            super().add(list(data.values()))

    def add(self, wordsData, isTaken=False):
        speechParts = State.getEntity("speechParts").get()
        step = 10
        for i in range(0, len(wordsData), step):
            data, frequencies = {}, {}
            # Save data in batches in order to avoid losing the whole progress in case of an error
            for j in range(i, min(i + step, len(wordsData)), 1):
                word = wordsData[j]

                # TODO figure out how to process phrases from the aforementioned file (can contain 2+ words as it
                #  turns out)
                data[word["lemma"]] = dict({
                    "word_lemma": word["lemma"].lower(),
                    "word_data": word["word"],
                    **({"word_translation": word["translation"]} if "translation" in word else {}),
                    "word_fk_speech_part_id": speechParts[word["speechPart"]]["uuid"],
                    "word_is_learn_taken": isTaken,
                    **({"word_article": word["article"]} if word["speechPart"].lower() == "noun" else {})
                })

                frequencies[word["lemma"]] = dict({
                    "functor": Corpus.getWordFrequency,
                    "params": ['deu', word["lemma"]],
                })

            for key, value in Requests.parallelRequests(frequencies).items():
                if value["result"] == 0:
                    data.pop(key, None)
                    continue

                data[key]["word_frequency"] = value["result"]

            super().add(list(data.values()))


