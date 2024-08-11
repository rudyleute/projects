import spacy
from collections import defaultdict
from spacy.parts_of_speech import IDS
from nltk.tokenize import sent_tokenize


class NLP:
    __langModelMap = dict({
        "german": "de_dep_news_trf",
        "english": "en_core_web_trf"
    })
    __genderArticleMap = defaultdict(str, {
        "Masc": "der",
        "Fem": "die",
        "Neut": "das"
    })
    __mainSpeechParts = {'VERB', 'NOUN', 'ADJ', 'AUX', 'ADV'}

    def __init__(self, lang):
        lang = lang.lower()
        self.__model = spacy.load(NLP.__langModelMap[lang])
        self.__lang = lang

    def isPhrase(self, text):
        counter, base = 0, None

        processed = self.processWords(text)
        base = processed[0]
        # Since there will not be a lot of words to iterate over, the overhead is not noticeable
        for elem in processed:
            if elem["speechPart"] in NLP.__mainSpeechParts:
                counter += 1
                base = elem

        isPhrase = counter >= 2 or (counter == 0 and len(text) >= 2)
        return isPhrase, base if not isPhrase else None

    @staticmethod
    def __parseTokens(docs):
        words = list()
        reprocess = set()

        for tokens in docs:
            for token in tokens:
                """
                If the capitalization of the lemma and the initial word do not match, it is highly likely
                that the pos_ tag is not correct. Since there is no direct generalization for tag_ and pos_ to a
                basic part of speech, this is an attempt to eliminated the implicit problem
                We change the capitalization and go with the result
                """
                # TODO add X words with changed capitalization to reprocessing
                # TODO nouns that do not have capital letters in lemma should be reprocessed
                if (isLower := token.text[0].islower()) != token.lemma_[0].islower():
                    text = token.text
                    if isLower and token.pos_.lower() != "noun":
                        text = text[0].upper() + text[1:]
                        reprocess.add(text)
                        continue
                    elif not isLower:
                        text = text[0].lower() + text[1:]
                        reprocess.add(text)
                        continue

                words.append(dict({
                    "word": token.text,
                    "lemma": token.lemma_,
                    "speechPart": token.pos_,
                    **({'article': NLP.__genderToArticle(token.morph.get("Gender"))} if token.pos_.lower() == "noun" else {})
                }))

        return words, reprocess

    @staticmethod
    def __genderToArticle(genderList):
        gender = list()
        for elem in genderList:
            gender.append(NLP.__genderArticleMap[elem])

        return '/'.join(gender)

    def processWords(self, words, batchSize=100):
        result = list()
        reprocess = set()

        # TODO use Leipzig corpora to generate a sentence for a WORD and then feed the sentence to the algorithm
        for curPos in range(0, len(words), batchSize):
            docs = list(self.__model.pipe(words[curPos: curPos + batchSize]))
            batchResult, toReprocess = NLP.__parseTokens(docs)
            reprocess = reprocess.union(set(toReprocess))

            result += batchResult

        # TODO get rid of copying the same rows as in the cycle above
        if len(reprocess) > 0:
            docs = list(self.__model.pipe(list(reprocess)))
            batchResult, toReprocess = NLP.__parseTokens(docs)

            result += batchResult

        return result

    def __splitText(self, text, size):
        # The text is split into sentences in order to preserve information for the NLP model,
        # and then the size constraint is satisfied
        sentences = sent_tokenize(text, language=self.__lang)
        texts = []

        # TODO take care of the situation, where the size is smaller than the size of the sentence
        curLen, chunkStart = 0, 0
        for curInd, sentence in enumerate(sentences):
            if len(sentence) + curLen <= size:
                curLen += len(sentence)
            else:
                curLen = len(sentence)
                texts.append(''.join(sentence[chunkStart: curInd + 1]))
                chunkStart = curInd + 1
        texts.append(''.join(sentences[chunkStart:]))

        return texts

    def processText(self, text):
        chunks = self.__splitText(text, self.__model.max_length)
        data = dict()

        for chunk in chunks:
            newData, reprocess = NLP.__parseTokens(self.__model(chunk))
            data |= newData
            chunks.append(list(reprocess))

        # TODO think of a better way to deduplicate data
        # TODO generally it makes sense to remove all the entries with the same pair (lemma, partOfSpeech)
        for key in data:
            unseen = list()
            for entry in data[key]:
                if entry not in unseen:
                    unseen.append(entry)

            data[key] = unseen

        return data

    @staticmethod
    def getSpeechPartsMapping():
        return {spacy.explain(pos): pos for pos in IDS if spacy.explain(pos) is not None}