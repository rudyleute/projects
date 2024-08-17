from abc import ABC, abstractmethod

from nltk.corpus import words

from State import State


class Tables(ABC):
    def __init__(self, tableName):
        self._tableName = tableName
        self._step = 10

    def get(self, params=None, isDict=True):
        data = dict({
            "from": self._tableName,
        })

        if params is not None:
            for key in ["limit", "where", "sort", "select"]:
                if key in params:
                    data[key] = params[key]

        return State.getConnection().select(data, isDict=isDict)

    def add(self, wordsData):
        data = dict({
            "from": self._tableName,
            "insert": wordsData
        })

        State.getConnection().insert(data)

    def update(self, wordsData):
        data = dict({
            "from": self._tableName,
            "update": wordsData,
        })

        State.getConnection().update(data)