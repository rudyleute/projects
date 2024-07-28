from Table import Table


class Conjugation(Table):
    def __init__(self, db):
        super().__init__(db, "conjugations")
