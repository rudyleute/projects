from Helpers.CSVParser import CSVParser
from Helpers.Corpus import Corpus
from State import State
from lingua import Language, LanguageDetectorBuilder
import langcodes
import re
from collections import defaultdict


class Manipulator:
    __langDetector = LanguageDetectorBuilder.from_languages(*[Language.ENGLISH, Language.GERMAN]).build()
    __phrases = "phrases"
    __words = "words"

    @staticmethod
    def __detectLanguage(text):
        language = Manipulator.__langDetector.detect_language_of(text)
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

                language = Manipulator.__detectLanguage(line[0])
                nlp = State.getNlp(language)

                isPhrase, base = nlp.isPhrase(line[0].split())
                base = base or {}

                base["word"] = line[0]
                if isPhrase:
                    base["lemma"] = line[0]

                if (language == State.getCurrentLang() and base["word"] in existingWords) or\
                    (language == State.getBaseLang() and base["word"] in emptyTranslations):
                    continue

                if len(line) == 2:
                    base["translation"] = line[1]

                words[language].setdefault(Manipulator.__phrases if isPhrase else Manipulator.__words, []).append(base)

        mapping = {
            State.getCurrentLang(): {
                Manipulator.__words: State.getEntity(Manipulator.__words).add,
                Manipulator.__phrases: State.getEntity(Manipulator.__phrases).add
            },
            State.getBaseLang(): {
                Manipulator.__words: State.getEntity(Manipulator.__words).addBaseLangData,
                Manipulator.__phrases: State.getEntity(Manipulator.__phrases).addBaseLangData
            }
        }

        for lang in words:
            for key in words[lang]:
                mapping[lang][key](words[lang][key])

    @staticmethod
    def processTeacherAi():
        result = CSVParser.readFile("active_vocabulary.csv", keyField="word", keyLower=True)

        """
        Remove the already existing duplicates (lemma form) in order to avoid overhead of retrieving a lot of info (especially API)
        in order to not use the data at all
        
        The date can be an alternative marker for not seen words, but it is not 100% correct, which is important in this case
        """
        existingWords = {row[0].lower() for row in State.getEntity("words").getWordsList()}
        for key in existingWords:
            result.pop(key, None)

        # Get all the information about the words (POS, lemma, article, etc)
        processed = State.getNlp("german").processWords(list(result.keys()))
        for elem in processed:
            try:
                elem["translation"] = result[elem["word"].lower()]["translation"]
            except KeyError:
                continue

        State.getEntity("words").add(processed, True)
