import bisect
from .Tables import Tables
from Helpers.Requests import Requests
from Helpers.Corpus import Corpus
from State import State
from collections import defaultdict


class Words(Tables):
    def __init__(self):
        super().__init__("word")
        self.__speechParts = State.getEntity("speechParts").get()
        self.__frequencies = State.getEntity("frequency").get(key="frequency_lowest_class")
        self.__nameUUID = {value["label"]: value["uuid"] for value in list(self.__frequencies.values())}

    def __getList(self, keys, params=None):
        if params is None:
            params = dict()
        params["select"] = list(keys)

        return self.get(params, isDict=False)

    def getWordsForUpdate(self, params=None):
        keys = ['word_id', 'word_lemma', 'word_translation', 'word_is_learn_taken']
        return [
            {
                key: result for key, result in zip(keys, value)
            } for value in self.__getList(keys, params)
        ]

    def getExistingWords(self):
        takenLemmas = {
            row[1]: row[2] if row[2] is not None else None
            for row in self.getWordsList(dict({
                "where": [
                    ("word_lemma", "is not", None),
                    ("word_is_learn_taken", "=", True)
                ]
            }))}
        nonTakenLemmas = {
            row[1]: {
                "uuid": row[0],
                "translation": row[2]
            }
            for row in self.getWordsList(dict({
                "where": [
                    ("word_lemma", "is not", None),
                    ("word_is_learn_taken", "=", False)
                ]
            }))}
        emptyTranslations = {row[2]: row[0] for row in self.getWordsList(dict({
            "where": [
                ("word_lemma", "is", None),
                ("word_translation", "is not", None)
            ]
        }))}

        return dict({
            "takenLemmas": takenLemmas,
            "nonTakenLemmas": nonTakenLemmas,
            "emptyTranslations": emptyTranslations
        })

    def getWordsList(self, params=None):
        return self.__getList(['word_id, word_lemma', "word_translation"], params)

    def add(self, wordsData, frequency=True, isLearnTaken=False, isArticleTaken=False):
        for i in range(0, len(wordsData), self._step):
            data, frequencies = {}, {}
            # Save data in batches in order to avoid losing the whole progress in case of an error
            for j in range(i, min(i + self._step, len(wordsData)), 1):
                word = wordsData[j]

                # TODO separate functions for base language and targetLanguage to avoid unnecessary checks
                isLemma = "lemma" in word
                data[(key := word["lemma"] if isLemma else word["translation"])] = dict({
                    **({"word_data": word["original"]} if isLemma else {}),
                    **({"word_lemma": word["lemma"]} if isLemma else {}),
                    **({"word_translation": word["translation"]} if "translation" in word else {}),
                    **({"word_fk_speech_part_id": self.__speechParts[word["speechPart"]][
                        "uuid"]} if "speechPart" in word else {}),
                    "word_fk_frequency_id": word["frequency"],
                    "word_is_learn_taken": isLearnTaken,
                    "word_is_article_taken": isArticleTaken,
                    **({"word_article": word["article"]} if "speechPart" in word and word["speechPart"].lower() == "noun" else {})
                })

                if data[key]["word_fk_frequency_id"] is None and frequency and isLemma:
                    frequencies[word["lemma"]] = dict({
                        "functor": Corpus.getWordFrequencyClass,
                        "params": ['deu', word["lemma"]],
                    })

            for key, value in Requests.parallelRequests(frequencies).items():
                if value["result"] is None:
                    data.pop(key, None)
                    continue

                data[key]["word_fk_frequency_id"] = self.__findFrequencyUUID(value["result"])

            super().add(list(data.values()))

    def __getFrequencyUUID(self, name):
        return self.__nameUUID[name] if name in self.__nameUUID else None

    def __findFrequencyUUID(self, freqClass):
        ind = bisect.bisect_right((segments := list(self.__frequencies.keys())), freqClass) - 1
        return self.__frequencies[segments[ind]]["uuid"]

    def update(self, wordsData, isLearnTaken=False):
        for i in range(0, len(wordsData), self._step):
            data = []
            # Save data in batches in order to avoid losing the whole progress in case of an error
            for j in range(i, min(i + self._step, len(wordsData)), 1):
                word = wordsData[j]

                data.append(dict({
                    "values": dict({
                        **({"word_lemma": word["lemma"]} if "lemma" in word else {}),
                        **({"word_translation": word["translation"]} if "translation" in word else {}),
                        "word_is_learn_taken": isLearnTaken
                    }),
                    "condition": [
                        ("word_id", '=', word["uuid"])
                    ]
                }))

            super().update(data)

    def getWordsToLearn(self, quantity=20):
        params = dict({
            "limit": quantity,
            "where": [
                ("word_is_learn_taken", "=", False),
                ("word_fk_speech_part_id", "!=", State.getEntity("speechParts").getPhrasesUuid()),
                ("word_lemma", "is not", None),

            ],
            "sort": [
                "word_frequency DESC"
            ]
        })

        return super().get(params=params, isDict=True)

    def getPhrasesToLearn(self, quantity=20):
        params = dict({
            "limit": quantity,
            "where": [
                ("word_is_learn_taken", "=", "False"),
                ("word_fk_speech_part_id", "=", State.getEntity("speechParts").getPhrasesUuid())
            ],
            "sort": [
                "'word_frequency' DESC"
            ]
        })

        return super().get(params=params, isDict=True)

    def getArticles(self, select=None, nonTaken=True):
        params = dict({
            **({"select": select} if isinstance(select, list) else {}),
            "where": [
                ("word_is_article_taken", "=", f"{'True' if not nonTaken else 'False'}"),
                ("word_fk_speech_part_id", "=", State.getEntity("speechParts").getUUID('noun')),
                ("word_lemma", "is not", None),
                ("word_article", "is not", None),
                ("word_translation", "is not", None)
            ]
        })

        for row in (result := super().get(params=params)):
            row["word_lemma"] = row["word_lemma"].title()

        return result
