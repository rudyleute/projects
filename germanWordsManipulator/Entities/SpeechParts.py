from .Tables import Tables
from Helpers.NLP import NLP


class SpeechParts(Tables):
    def __init__(self):
        super().__init__("speech_part")

    def save(self):
        speechParts = NLP.getSpeechPartsMapping()
        insert = []
        for key in speechParts:
            insert.append(dict({
                "speech_part_model_name": speechParts[key],
                "speech_part_name": key
            }))
        self.add(insert)

    def get(self, params=None, isDict=True):
        result = super().get(params, isDict=isDict)
        data = dict()

        for oneRow in result:
            data[oneRow["speech_part_model_name"]] = dict({
                "uuid": oneRow["speech_part_id"],
                "name": oneRow["speech_part_name"]
            })

        return data

    def getCode(self, name):
        return super().get({
            "select": ["speech_part_model_name"],
            "where": [
                ("speech_part_name", "=", name)
            ]
        }, False)[0][0]

    def getUuid(self, name):
        return super().get({
            "select": ["speech_part_id"],
            "where": [
                ("speech_part_name", "=", name)
            ]
        }, False)[0][0]

    def getPhrasesCode(self):
        return self.getCode("phrase")

    def getPhrasesUuid(self):
        return self.getUuid("phrase")
