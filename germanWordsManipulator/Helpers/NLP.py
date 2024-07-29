import spacy
from nltk.tokenize import sent_tokenize


class NLP:
    __langModelMap = dict({
        "german": "de_dep_news_trf"
    })

    def __init__(self, lang):
        lang = lang.lower()
        self.__model = spacy.load(NLP.__langModelMap[lang])
        self.__lang = lang

    @staticmethod
    def __parseTokens(tokens):
        words = dict()

        for token in tokens:
            words.setdefault(token.pos_, []).append(dict({
                "word": token.text,
                "lemma": token.lemma_,
                "partOfSpeechCode": token.pos_
            }))

        return words

    def processWord(self, word):
        return list(NLP.__parseTokens(self.__model(word)).values())[0]

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
            data |= NLP.__parseTokens(self.__model(chunk))

        # TODO think of a better way to deduplicate data
        # TODO generally it makes sense to remove all the entries with the same pair (lemma, partOfSpeech)
        for key in data:
            unseen = list()
            for entry in data[key]:
                if entry not in unseen:
                    unseen.append(entry)

            data[key] = unseen

        return data
