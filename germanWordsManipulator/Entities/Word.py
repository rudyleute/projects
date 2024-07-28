from Table import Table

class Word(Table):
    def __init__(self, db):
        super().__init__(db, "words")
