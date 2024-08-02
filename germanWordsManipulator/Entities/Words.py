from .Tables import Tables
from collections import defaultdict


class Words(Tables):
    def __init__(self, db):
        super().__init__(db, "word")

    def getWordsList(self, params=None):
        if params is None:
            params = dict()
        params["select"] = {'word_name'}

        return self.get(params, isDict=False)


