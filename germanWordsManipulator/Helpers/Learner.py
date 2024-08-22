from State import State


class Learner:
    @staticmethod
    def learnWords(quantity=25):
        words = State.getEntity("words").getWordsToLearn(quantity)
        uuids = list()
        for word in words:
            uuids.append(dict({"uuid": word["word_id"]}))
            print(f"{word['word_data']}\t{word['word_lemma']}")

        # State.getEntity("words").update(uuids, isLearnTaken=True)




