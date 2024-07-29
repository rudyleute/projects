from .Tables import Tables


class Conjugations(Tables):
    def __init__(self, db):
        super().__init__(db, "conjugations")
