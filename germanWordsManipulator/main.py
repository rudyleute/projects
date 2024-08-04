from DB import DB
from Entities.Words import Words
from Entities.SpeechParts import SpeechParts
from Entities.Phrases import Phrases
from Helpers.NLP import NLP
from Manipulator import Manipulator
from State import State
import os

from dotenv import load_dotenv

load_dotenv()


def main():
    db = DB(os.getenv('DB_NAME'), os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD'))

    State.init(db, dict({
        "german": NLP("german"),
        "english": NLP("english")
    }), dict({
        "words": Words(),
        "speechParts": SpeechParts()
    }), "german")
    State.addEntity("phrases", Phrases())

    m = Manipulator()
    m.processTeacherAi()
    m.processTextFile("/home/otto/Desktop/GermanWordsToLearn.txt")


if __name__ == "__main__":
    main()
