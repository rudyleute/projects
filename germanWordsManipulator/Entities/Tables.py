from abc import ABC, abstractmethod


class Tables(ABC):
    def __init__(self, db, tableName):
        self._db = db
        self._tableName = tableName

    def get(self, params=None, isDict=True):
        data = dict({
            "from": self._tableName,
        })

        if params is not None:
            for key in ["limit", "where", "sort", "select"]:
                if key in params:
                    data[key] = params[key]

        return self._db.select(data, isDict=isDict)

    def add(self, wordsData):
        data = dict({
            "from": self._tableName,
            "insert": wordsData
        })

        self._db.insert(data)