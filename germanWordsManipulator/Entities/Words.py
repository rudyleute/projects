from .Tables import Tables


class Words(Tables):
    def __init__(self, db):
        super().__init__(db, "word")
