from Helpers.CSVParser import CSVParser
from Helpers.Corpora import Corpus
import spacy
from concurrent.futures import ThreadPoolExecutor


class Manipulator:
    def __init__(self, db, nlp, speechPart, words):
        self.__db = db
        self.__nlp = nlp
        self.__speechPart = speechPart
        self.__words = words

    @staticmethod
    def __parallelRequests(data):
        dataCopy = data.copy()
        with ThreadPoolExecutor() as executor:
            futures = []
            for key, task in dataCopy.items():
                futures.append(executor.submit(task["functor"], *task["params"]))

            results = [future.result() for future in futures]
            for key, result in zip(dataCopy.keys(), results):
                dataCopy[key]["result"] = result

            return dataCopy

    def processTextFile(self, filename, delim='('):
        with open(filename, 'r') as file:
            """
            1. Separate into languages
            2. Separate into categories like "phrases" and others
            3. Find the main word
            4. Find a lemma
            """

            raise NotImplemented



    def processTeacherAi(self):
        result = CSVParser.readFile("active_vocabulary.csv", keyField="word", keyLower=True)
        speechParts = self.__speechPart.get()

        """
        Remove the already existing duplicates (lemma form) in order to avoid overhead of retrieving a lot of info (especially API)
        in order to not use the data at all
        
        The date can be an alternative marker for not seen words, but it is not 100% correct, which is important in this case
        """
        existingWords = {row[0].lower() for row in self.__words.getWordsList()}
        for key in existingWords:
            result.pop(key, None)

        # Get all the information about the words (POS, lemma, article, etc)
        processed = self.__nlp.processWords(list(result.keys()))

        step = 10
        for i in range(0, len(processed), step):
            data, frequencies = {}, {}
            # Save data in batches in order to avoid losing the whole progress in case of an error
            for j in range(i, min(i + step, len(processed)), 1):
                word = processed[j]

                # TODO figure out how to process phrases from the aforementioned file (can contain 2+ words as it
                #  turns out)
                # Word["word"] does not have to be in result (difference with existingWords,
                # but can occur in a processed phrase)
                try:
                    data[word["lemma"]] = dict({
                        "word_lemma": word["lemma"].lower(),
                        "word_data": word["lemma"].lower(),
                        "word_translation": result[word["word"]]["translation"],
                        "word_fk_speech_part_id": speechParts[word["speechPart"]]["uuid"],
                        "word_is_learn_taken": True,
                        **({"word_article": word["article"]} if word["speechPart"].lower() == "noun" else {})
                    })

                    frequencies[word["lemma"]] = dict({
                        "functor": Corpus.getWordFrequency,
                        "params": ['deu', word["lemma"]],
                    })
                except KeyError:
                    continue

            for key, value in Manipulator.__parallelRequests(frequencies).items():
                if value["result"] == 0:
                    data.pop(key, None)
                    continue

                data[key]["word_frequency"] = value["result"]

            self.__words.add(list(data.values()))
