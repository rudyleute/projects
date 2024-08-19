from Helpers.CSVParser import CSVParser
from State import State
from Helpers.Corpus import Corpus
from lingua import Language, LanguageDetectorBuilder
from collections import defaultdict
from Helpers.Requests import Requests
from Helpers.PDFParser import PDFParser
import langcodes
import re


class Processor:
    __langDetector = LanguageDetectorBuilder.from_languages(*[Language.ENGLISH, Language.GERMAN]).build()
    __phrases = "phrases"
    __words = "words"

    @staticmethod
    def __detectLanguage(text):
        # TODO this should not be hardcoded
        base = Processor.__langDetector.compute_language_confidence(text, Language.ENGLISH)
        target = Processor.__langDetector.compute_language_confidence(text, Language.GERMAN)
        language = Language.ENGLISH if base - target > 0.3 else Language.GERMAN

        return langcodes.get(language.iso_code_639_1.name.lower()).display_name().lower()

    @staticmethod
    def processTextFile(filename, lang=None):
        words = defaultdict(dict)

        with open(filename, 'r', encoding="utf-8-sig") as file:
            data = [line.strip() for line in file.readlines() if len(line.strip()) > 0]

        edited = dict()
        for line in data:
            line = [part.strip() for part in re.split(r"\(|\)", line.strip())]

            value = dict()
            value["word"] = line[0]
            if len(line) >= 2:
                value["translation"] = line[1]

            edited[line[0]] = value

        Processor.__addValues(Processor.__process(edited, removeExistent=False), False)

    @staticmethod
    def __alterExistent(data, toRemove):
        targetLang, baseLang = State.getTargetLang(), State.getBaseLang()
        result = dict()
        existingWords = State.getEntity("words").getExistingWords()

        if targetLang in data:
            # TODO check that the key is not present in word_data
            forSentences = {
                key: dict({
                    "functor": Corpus.getExampleSentence,
                    "params": ['deu', key],
                })
                for key in data[targetLang]
                if key not in existingWords["takenLemmas"] and key not in existingWords["nonTakenLemmas"]
            }

            sentences = Requests.parallelRequests(forSentences)
            sentencesToProcess = dict()
            for key in sentences:
                sentencesToProcess[key] = sentences[key]["result"][0]

            targetResult = defaultdict(dict)
            processedWords = State.getNlp(targetLang).processSentences(sentencesToProcess)
            for key, value in processedWords.items():
                if key in existingWords["takenLemmas"] or \
                        (toRemove and key in existingWords["nonTakenLemmas"]):
                    continue

                word = value["word"]
                value["original"] = data[targetLang][word]["word"]
                spType = Processor.__words if data[targetLang][word]["main"] is not None else Processor.__phrases

                if toRemove and word in existingWords["nonTakenLemmas"] \
                        and existingWords["nonTakenLemmas"][word]["translation"] is not None:
                    targetResult[spType].setdefault("updateLearn", []).append(
                        existingWords["nonTakenLemmas"][word]["uuid"])
                    continue

                if "translation" in data[targetLang][value["word"]]:
                    if (translation := data[targetLang][value["word"]]["translation"]) in existingWords[
                        "emptyTranslations"]:
                        targetResult[spType].setdefault("update", []).append(dict({
                            "uuid": existingWords["emptyTranslations"][translation],
                            "lemma": value["lemma"]
                        }))
                        continue

                    value["translation"] = data[targetLang][value["word"]]["translation"]

                value["frequency"] = data[targetLang][value["word"]]["frequency"]
                targetResult[spType].setdefault("add", []).append(value)

            result[targetLang] = targetResult

            if baseLang in data:
                baseResult = defaultdict(dict)
                for key, value in data[baseLang].items():
                    if value["word"] not in existingWords["emptyTranslations"]:
                        baseResult[Processor.__words if value["main"] is not None else Processor.__phrases] \
                            .setdefault("add", []).append(
                            {
                                "translation": value["word"],
                                "frequency": data[baseLang][value["main"] or value["word"]]["frequency"]
                            })

                result[baseLang] = baseResult

        return result

    @staticmethod
    def __process(data, removeExistent, freqUUID=None, onlyTarget=False, defaultLang=None):
        """
        Remove the already existing duplicates (lemma form) in order to avoid overhead of retrieving a lot of info (especially API)
        in order to not use the data at all
        """
        language = dict({
            State.getBaseLang(): defaultdict(dict),
            State.getTargetLang(): defaultdict(dict)
        })
        for key, value in data.items():
            lang = defaultLang or Processor.__detectLanguage(key)

            value["language"] = lang
            value["frequency"] = freqUUID
            value["main"] = State.getNlp(lang).getBase(key)
            value["word"] = key
            language[lang][key if value["main"] is None else value["main"]] = value

        if onlyTarget:
            language.pop(State.getBaseLang(), None)

        # TODO sentences and everything should be factored out to here
        return Processor.__alterExistent(language, toRemove=removeExistent)

    @staticmethod
    def processTeacherAi(removeExistent=True, determineLanguage=True):
        result = CSVParser.readFile("active_vocabulary.csv", keyField="word", keyLower=True)

        # Get all the information about the words (POS, lemma, article, etc)
        processed = Processor.__process(result, removeExistent=removeExistent, onlyTarget=True)
        Processor.__addValues(processed, True)

    @staticmethod
    def __addValues(processed, isLearnTaken):
        for language in processed:
            for spType in processed[language]:
                for funcName in processed[language][spType]:
                    if funcName == "add":
                        State.getEntity(spType).add(processed[language][spType][funcName], isLearnTaken=isLearnTaken)
                    elif funcName == "update":
                        State.getEntity(spType).update(processed[language][spType][funcName], isLearnTaken=isLearnTaken)
                    elif funcName == "updateLearn":
                        State.getEntity(spType).update(processed[language][spType][funcName], isLearnTaken=isLearnTaken)

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
        processed = Processor.__process(data, True)
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
    def processGoethe(filename, freqUUID):
        result = PDFParser.parseGoethe(filename)
        if result is not None:
            prepared = {value: dict({"word": value}) for value in list(result.keys())}
            processed = Processor.__process(prepared, removeExistent=False, defaultLang="german", freqUUID=freqUUID)
            Processor.__addValues(processed, False)

    # @staticmethod
    # def exportArticles(order, filename="articles"):
    #     articles = State.getEntity("words").getArticles(order)
    #
    #     CSVParser.editFile(f"{filename}.csv", articles, hasHeader=True)
