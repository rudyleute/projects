from DB import DB
from Entities.Words import Words
from Entities.SpeechParts import SpeechParts
from Entities.Phrases import Phrases
from Helpers.NLP import NLP
from Helpers.Processor import Processor
from Helpers.Learner import Learner
from State import State
import os
from Helpers.Corpus import Corpus

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

    # Processor.exportArticles(["word_lemma", "word_article", "word_translation"])
    Processor.processTextFile("/home/otto/Desktop/UsefulWords.txt", "english")
    Processor.processTextFile("/home/otto/Desktop/GermanWordsToLearn.txt")

if __name__ == "__main__":
    main()
