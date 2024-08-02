from Helpers.CSVParser import CSVParser
from Helpers.Corpora import Corpus
import spacy


class Manipulator:
    def __init__(self, db, nlp, speechPart, words):
        self.__db = db
        self.__nlp = nlp
        self.__speechPart = speechPart
        self.__words = words

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
        processed = self.__nlp.processWords(list(result.keys()))[:5]

        step = 10
        for i in range(0, len(processed), step):
            data = []
            # Save data in batches in order to avoid losing the whole progress in case of an error
            for j in range(i, min(i + step, len(processed)), 1):
                word = processed[j]

                # TODO figure out how to process phrases from the aforementioned file (can contain 2+ words as it
                #  turns out)
                # Word["word"] does not have to be in result (difference with existingWords,
                # but can occur in a processed phrase)
                try:
                    wordData = dict({
                        "word_name": word["lemma"].lower(),
                        "word_translation": result[word["word"]]["translation"],
                        "word_fk_speech_part_id": speechParts[word["speechPart"]]["id"],
                        "word_is_learn_taken": True,
                        "word_frequency": Corpus.getWordFrequency('deu', word["lemma"]),
                        **({"word_article": word["article"]} if word["speechPart"].lower() == "noun" else {})
                    })
                except KeyError:
                    continue

                if wordData["word_frequency"] == 0:
                    continue

                data.append(wordData)

            self.__words.add(data)