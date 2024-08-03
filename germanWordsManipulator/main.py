from DB import DB
from Entities.Words import Words
from Entities.SpeechParts import SpeechParts
from Helpers.NLP import NLP
from Manipulator import Manipulator
from State import State
import os

from dotenv import load_dotenv

load_dotenv()


def main():
    db = DB(os.getenv('DB_NAME'), os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD'))
    words = Words()
    speechParts = SpeechParts()
    nlp = NLP("german")

    State.init(db, dict({
        "german": nlp
    }), dict({
        "words": words,
        "speechParts": speechParts
    }))

    m = Manipulator()
    m.processTeacherAi()
    # m.processTextFile("~/Desktop/GermanWordsToLearn.odt")


if __name__ == "__main__":
    main()
