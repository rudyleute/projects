import requests


class Corpus:
    __apiAddress = "https://api.wortschatz-leipzig.de/ws"

    @staticmethod
    def __request(url, reqType="get"):
        result = requests.request(reqType, url)
        if result.ok:
            return result.json()

        raise Exception(f"{url} finished with the code {result.status_code}: {result.reason}")

    @staticmethod
    def getCorpora():
        url = f"{Corpus.__apiAddress}/corpora"
        return Corpus.__request(url)

    @staticmethod
    def getLanguageCorpora(code):
        if len(code) != 3:
            raise Exception("Incorrect language code")

        corpora = Corpus.getCorpora()
        corporaData, corpusNameMap = dict(), dict()

        """
        We are interested only in corpora that belongs to the language we are interested in
        Besides, we want to maximize the number of sentence for each type of the corpora, and at the same time we want
        the variety of different types as they potentially give us different types of text (style wise)
        
        Type of the corpora - name of the corpus without the postfix as postfix denotes the number of sentences
        For instance, deu_news_2012_3M is the name of the corpus. The type's name is deu_news_2012
        """

        for corpus in corpora:
            if corpus["corpusName"].startswith(code):
                noPostfix = ''.join((corpus["corpusName"].split('_'))[:-1])
                if noPostfix not in corporaData or corporaData[noPostfix] < corpus["numberOfSentences"]:
                    corporaData[noPostfix] = corpus["numberOfSentences"]
                    corpusNameMap[noPostfix] = corpus["corpusName"]

        if len(corporaData) == 0:
            return dict()

        # We may want to adjust the contribution to the frequency based on the site of the sentences' pool
        return {corpusNameMap[noPostfix]: corporaData[noPostfix] for noPostfix in corporaData}

    @staticmethod
    def getWordFrequency(code, word):
        corporaData = Corpus.getLanguageCorpora(code)
        corporaNames = list(corporaData.keys())

        freq = 0
        for name in corporaNames:
            url = f"{Corpus.__apiAddress}/words/{name}/word/{word}"
            freq += (Corpus.__request(url))["freq"]

        return freq
