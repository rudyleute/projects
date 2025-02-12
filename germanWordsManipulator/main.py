from DB import DB
from Entities.Words import Words
from Entities.SpeechParts import SpeechParts
from Entities.Phrases import Phrases
from Entities.Frequency import Frequency
from Helpers.NLP import NLP
from Helpers.Processor import Processor
from Helpers.PDFParser import PDFParser
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
        "speechParts": SpeechParts(),
        "frequency": Frequency()
    }), "german")
    State.addEntity("words", Words())
    State.addEntity("phrases", Phrases())

    # Processor.exportArticles(["word_lemma", "word_article", "word_translation"])
    # Processor.processGoethe("Goethe-Zertifikat_B1_Wortliste.pdf", freqUUID="ff59eb98-e477-4c07-9181-9d98d9526e7f")
    # Processor.processTextFile("/home/otto/Desktop/Gits/projects/germanWordsManipulator/GermanWordsToLearn.txt")
    # Processor.processTextFile("/home/otto/Desktop/UsefulWords.txt")
    # Processor.processTeacherAi()
    Learner.learnWords(30)

if __name__ == "__main__":
    main()
