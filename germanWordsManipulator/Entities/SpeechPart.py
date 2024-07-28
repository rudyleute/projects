from Table import Table


class SpeechPart(Table):
    def __init__(self, db):
        super().__init__(db, "speech_parts")
