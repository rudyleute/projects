from Helpers.CSVParser import CSVParser
from State import State
from Helpers.Corpus import Corpus
from lingua import Language, LanguageDetectorBuilder
import langcodes
import re
from collections import defaultdict
from Helpers.Requests import Requests


class Processor:
    __langDetector = LanguageDetectorBuilder.from_languages(*[Language.ENGLISH, Language.GERMAN]).build()
    __phrases = "phrases"
    __words = "words"

    @staticmethod
    def __detectLanguage(text):
        # TODO this should not be hardcoded
        base = Processor.__langDetector.compute_language_confidence(text, Language.ENGLISH)
        target = Processor.__langDetector.compute_language_confidence(text, Language.GERMAN)
        language = Language.ENGLISH if base - target > 0.4 else Language.GERMAN

        return langcodes.get(language.iso_code_639_1.name.lower()).display_name().lower()

    @staticmethod
    def processTextFile(filename, lang=None):
        words = defaultdict(dict)
        # We do not merge them as some words in English can be exactly the same as the words in German and vice versa
        existingWords = {row[0].lower() for row in State.getEntity("words").getWordsList(dict({
            "where": [
                ("word_lemma", "is not", None)
            ]
        }))}
        emptyTranslations = {row[0].lower() for row in State.getEntity("words").getTranslationsList(dict({
            "where": [
                ("word_lemma", "is", None),
                ("word_translation", "is not", None)
            ]
        }))}

        with open(filename, 'r', encoding="utf-8-sig") as file:
            data = [line.strip() for line in file.readlines() if len(line.strip()) > 0]

        baseLang, targetLang = State.getBaseLang(), State.getTargetLang()
        store, forSentences = dict({baseLang: dict(), targetLang: dict()}), dict()
        for line in data:
            line = [part.strip() for part in re.split(r"\(|\)", line.strip())]
            # TODO this can be done in a better way
            language = lang if lang is not None else Processor.__detectLanguage(line[0])
            main = State.getNlp(language).getBase(line[0])

            if (language == targetLang and line[0].lower() in existingWords) or \
                    (language == baseLang and line[0].lower() in emptyTranslations):
                continue

            # main is the original format of the word, not its lemma
            if main is not None and ((language == targetLang and main.lower() not in existingWords) or \
                                     (language == baseLang and main.lower() not in emptyTranslations)):
                # TODO the language code must not be hardcoded
                if language == targetLang:
                    forSentences[main] = dict({
                        "functor": Corpus.getExampleSentence,
                        "params": ['deu', main],
                    })

                    store[main] = {
                        "main": main,
                        "original": line[0],
                        "translation": line[1] if len(line) == 2 else None,
                        "language": language
                    }
                else:
                    words[language].setdefault(Processor.__words, []).append({
                        "lemma": line[0],
                        "word": line[0]
                    })
                continue

            words[language].setdefault(Processor.__phrases, []).append({
                "lemma": line[0],
                "word": line[0]
            })

        sentences = Requests.parallelRequests(forSentences)
        # TODO can probably be optimized for the cases where the sentences for different words are the same
        sentencesToProcess = dict()
        for key in sentences:
            store[key]["sentence"] = sentences[key]["result"][0]
            sentencesToProcess[key] = store[key]["sentence"]

        processed = {
            lemma: value for lemma, value in
            State.getNlp(targetLang).processSentences(sentencesToProcess).items()
            if lemma not in existingWords
        }
        words[targetLang].setdefault(Processor.__words, list(processed.values()))

        mapping = {
            targetLang: {
                Processor.__words: State.getEntity(Processor.__words).add,
                Processor.__phrases: State.getEntity(Processor.__phrases).add
            },
            baseLang: {
                Processor.__words: State.getEntity(Processor.__words).addBaseLangData,
                Processor.__phrases: State.getEntity(Processor.__phrases).addBaseLangData
            }
        }

        for lang in words:
            for key in words[lang]:
                mapping[lang][key](words[lang][key])

    @staticmethod
    def __removeExistent(data):
        dataCopy = data.copy()

        existingWords = {row[0].lower() for row in State.getEntity("words").getWordsList(dict({
            "where": [
                ("word_lemma", "is not", None)
            ]
        }))}
        for key in existingWords:
            dataCopy.pop(key, None)

        return dataCopy

    @staticmethod
    def __process(data):
        """
        Remove the already existing duplicates (lemma form) in order to avoid overhead of retrieving a lot of info (especially API)
        in order to not use the data at all
        """
        unique = Processor.__removeExistent(data)
        return State.getNlp(State.getTargetLang()).processWords(list(unique.keys()))

    @staticmethod
    def processTeacherAi():
        result = CSVParser.readFile("active_vocabulary.csv", keyField="word", keyLower=True)

        # Get all the information about the words (POS, lemma, article, etc)
        processed = Processor.__process(result)
        for elem in processed:
            try:
                elem["translation"] = result[elem["word"].lower()]["translation"]
            except KeyError:
                continue

        State.getEntity("words").add(processed, isLearnTaken=True)

    @staticmethod
    def __getCopyName(filename):
        split = filename.split('.')
        split[0] += "_copy"
        return '.'.join(split)

    @staticmethod
    def parseArticles(filename, delim='\t'):
        # add headers in order to use the csv parser effectively
        with open(filename, 'r') as file:
            lines = file.readlines()[2:]

        # We use the copy in order to not modify the original file
        copyFilename = Processor.__getCopyName(filename)
        with open(copyFilename, 'w') as copyFile:
            copyFile.write(''.join(["word\tarticle\ttranslation\n"] + lines))

        data = CSVParser.readFile(copyFilename, delim=delim, keyLower=True, keyField="word")
        processed = Processor.__process(data)
        nounCode = State.getEntity("speechParts").getCode("noun")

        for wordData in processed:
            if "article" not in wordData:
                wordData["article"] = data[wordData["word"]]["article"]

            # Try to ensure correct lemmization, but if the determined speechPart is not a noun,
            # we have to work with what we have
            if wordData["speechPart"] != nounCode:
                wordData["lemma"] = wordData["word"].title()
            else:
                wordData["lemma"] = wordData["lemma"].title()

            wordData["speechPart"] = nounCode
            wordData["translation"] = data[wordData["word"]]["translation"]

        State.getEntity("words").add(processed, isArticleTaken=True)

    @staticmethod
    def exportArticles(order, filename="articles"):
        articles = State.getEntity("words").getArticles(order)

        CSVParser.editFile(f"{filename}.csv", articles, hasHeader=True)
