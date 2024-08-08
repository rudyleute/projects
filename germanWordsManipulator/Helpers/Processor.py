from Helpers.CSVParser import CSVParser
from State import State
from lingua import Language, LanguageDetectorBuilder
import langcodes
import re
from collections import defaultdict


class Processor:
    __langDetector = LanguageDetectorBuilder.from_languages(*[Language.ENGLISH, Language.GERMAN]).build()
    __phrases = "phrases"
    __words = "words"

    @staticmethod
    def __detectLanguage(text):
        language = Processor.__langDetector.detect_language_of(text)
        return langcodes.get(language.iso_code_639_1.name.lower()).display_name().lower()

    @staticmethod
    def processTextFile(filename):
        words = defaultdict(dict)
        existingWords = {row[0].lower() for row in State.getEntity("words").getWordsList(dict({
            "where": [
                ("word_lemma", "is not", None)
            ]
        }))}
        emptyTranslations = {row[0].lower() for row in State.getEntity("words").getTranslationsList(dict({
            "where": [
                ("word_lemma", "is", None)
            ]
        }))}

        with open(filename, 'r', encoding="utf-8-sig") as file:
            for line in file:
                line = re.split(r"\(|\)", line.strip())
                line = [part.strip() for part in line if part.strip()]
                if len(line) == 0:
                    continue

                language = Processor.__detectLanguage(line[0])
                nlp = State.getNlp(language)

                isPhrase, base = nlp.isPhrase(line[0].split())
                base = base or {}

                base["word"] = line[0]
                if isPhrase:
                    base["lemma"] = line[0]

                if (language == State.getCurrentLang() and base["word"] in existingWords) or \
                        (language == State.getBaseLang() and base["word"] in emptyTranslations):
                    continue

                if len(line) == 2:
                    base["translation"] = line[1]

                words[language].setdefault(Processor.__phrases if isPhrase else Processor.__words, []).append(base)

        mapping = {
            State.getCurrentLang(): {
                Processor.__words: State.getEntity(Processor.__words).add,
                Processor.__phrases: State.getEntity(Processor.__phrases).add
            },
            State.getBaseLang(): {
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
        return State.getNlp(State.getCurrentLang()).processWords(list(unique.keys()))

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

        State.getEntity("words").add(processed, True)

    @staticmethod
    def __getCopyName(filename):
        split = filename.split('.')
        split[0] += "_copy"
        return '.'.join(split)

    @staticmethod
    def parseArticlesForNouns(filename, delim='\t'):
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
