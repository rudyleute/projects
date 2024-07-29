from Helpers.NLP import NLP
from DB import DB


class Manipulator:
    def __init__(self, db, nlp):
        self.__db = db
        self.__nlp = nlp

