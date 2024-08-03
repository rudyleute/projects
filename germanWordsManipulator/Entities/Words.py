from .Tables import Tables
from collections import defaultdict


class Words(Tables):
    def __init__(self):
        super().__init__("word")

    def getWordsList(self, params=None):
        if params is None:
            params = dict()
        params["select"] = {'word_lemma'}

        return self.get(params, isDict=False)


