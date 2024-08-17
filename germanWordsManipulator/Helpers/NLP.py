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
    __baseIgnore = {"etw", "jdn", "jdm", "etwas", "jemanden", "jemandem"}

    def __init__(self, lang):
        lang = lang.lower()
        self.__model = spacy.load(NLP.__langModelMap[lang])
        self.__lang = lang

    def getBase(self, text):
        counter, base = 0, None

        # etw, jdn, etc. are often misclassified which affects the separation the words into word-centered text and
        # phrases
        processed = {key: value for key, value in self.processText(text).items() if key not in NLP.__baseIgnore}
        if len(processed) == 0:
            return text

        base = list(processed.keys())[0]
        # Since there will not be a lot of words to iterate over, the overhead is not noticeable
        for key, elem in processed.items():
            if elem["speechPart"] in NLP.__mainSpeechParts:
                counter += 1
                base = key

        isPhrase = counter >= 2 or (counter == 0 and len(processed) >= 2)
        return base if not isPhrase else None

    @staticmethod
    def __parseTokens(docs):
        words = dict()

        for tokens in docs:
            for token in tokens if not isinstance(tokens, spacy.tokens.Token) else [tokens]:
                # TODO there should be a better way to remove misclassified languages
                if token.pos_ != "X":
                    words[token.text] = dict({
                        "word": token.text,
                        "lemma": token.lemma_,
                        "speechPart": token.pos_,
                        **({'article': NLP.__genderToArticle(
                            token.morph.get("Gender"))} if token.pos_.lower() == "noun" else {})
                    })

        return words

    @staticmethod
    def __genderToArticle(genderList):
        gender = list()
        for elem in genderList:
            gender.append(NLP.__genderArticleMap[elem])

        return '/'.join(gender)

    def processWords(self, words, batchSize=100):
        result = dict()

        # TODO use Leipzig corpora to generate a sentence for a WORD and then feed the sentence to the algorithm
        for curPos in range(0, len(words), batchSize):
            docs = list(self.__model.pipe(words[curPos: curPos + batchSize]))
            batchResult = NLP.__parseTokens(docs)
            result.update(batchResult)

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

    def processSentences(self, sentences):
        result = dict()
        processed = list(self.__model.pipe(list(sentences.values())))

        for value in zip(list(sentences.keys()), processed):
            for token in value[1]:
                if token.text == value[0]:
                    if token.pos_ == "X":
                        continue

                    result[token.text] = dict({
                        "word": token.text,
                        "speechPart": token.pos_,
                        "lemma": token.lemma_,
                        **({'article': NLP.__genderToArticle(
                            token.morph.get("Gender"))} if token.pos_.lower() == "noun" else {})
                    })

                    break

        return result

    def processText(self, text):
        chunks = self.__splitText(text, self.__model.max_length)
        data = dict()

        for chunk in chunks:
            newData = NLP.__parseTokens(self.__model(chunk))
            data.update(newData)

        return data

    @staticmethod
    def getSpeechPartsMapping():
        return {spacy.explain(pos): pos for pos in IDS if spacy.explain(pos) is not None}
