from abc import ABC


class State(ABC):
    _db = None
    _nlps = dict()
    _entities = dict()

    @staticmethod
    def init(connection, nlpsData, entitiesData):
        State.setConnection(connection)
        State.addNlps(nlpsData)
        State.addEntities(entitiesData)

    @staticmethod
    def setConnection(connection):
        State._db = connection

    @staticmethod
    def getConnection():
        return State._db

    @staticmethod
    def getBaseNlp():
        return State.getNlp("english")

    @staticmethod
    def getNlp(language):
        return State._nlps[language]

    @staticmethod
    def getEntity(name):
        return State._entities[name]

    @staticmethod
    def addNlp(language, nlp):
        State._nlps[language] = nlp

    @staticmethod
    def addNlps(data):
        for key in data:
            State.addNlp(key, data[key])

    @staticmethod
    def addEntity(name, entity):
        State._entities[name] = entity

    @staticmethod
    def addEntities(data):
        for key in data:
            State.addEntity(key, data[key])