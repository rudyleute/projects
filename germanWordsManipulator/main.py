from DB import DB
from Entities.Words import Words
from Entities.SpeechParts import SpeechParts
from Helpers.NLP import NLP
from Manipulator import Manipulator
import os

from dotenv import load_dotenv
load_dotenv()


def main():
    db = DB(os.getenv('DB_NAME'), os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD'))
    words = Words(db)
    speechParts = SpeechParts(db)
    nlp = NLP("german")

    m = Manipulator(db, nlp, speechParts, words)
    m.processTeacherAi()


if __name__ == "__main__":
    main()
