from .Tables import Tables
from Helpers.NLP import NLP


class SpeechParts(Tables):
    def __init__(self, db):
        super().__init__(db, "speech_part")

    def save(self):
        speechParts = NLP.getSpeechPartsMapping()
        insert = []
        for key in speechParts:
            insert.append(dict({
                "speech_part_model_name": speechParts[key],
                "speech_part_name": key
            }))
        self.add(insert)
