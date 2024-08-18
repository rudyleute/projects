from collections import defaultdict
import fitz
import re
from State import State


class PDFParser:
    @staticmethod
    def readPdf(filename, phrase, lm=0, rm=0, tm=0, bm=0):
        doc = fitz.open(filename)
        pages, isPhraseFound = [], False

        # Iterate through all the pages
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_width, page_height = page.rect.width, page.rect.height

            # Define the area to extract text from (ignoring margins)
            rect = fitz.Rect(lm, tm, page_width - rm, page_height - bm)
            text = page.get_text("text", clip=rect)

            # If the phrase has already been found, just collect all remaining text
            if isPhraseFound:
                pages.append(text)
                continue

            # Search for the phrase in the extracted text
            startInd = text.find(phrase)
            if startInd != -1:
                isPhraseFound = True
                # TODO this is adjusted for reading Goethe pdfs, when sth else is needed, the indexing should be changed
                pages.append('\n' + text[:startInd])

        return pages if isPhraseFound else None

    @staticmethod
    def parseGoethe(filename):
        text = ''.join(PDFParser.readPdf(filename, "ALPHABETISCHER WORTSCHATZ", 30, 10, 50, 50)[:-1])
        splitText = [splitValue for value in text.split('\n')
                     if len((splitValue := [part for part in re.split(r'(\s)\s+', value) if part])) > 0]

        lastKey, waitForCont, result = None, False, defaultdict(list)
        for i in range(len(splitText)):
            if len(splitText[i]) == 3:
                key = re.split(r',|\(|-', splitText[i][0])[0].strip()
                if len(key) == 0 and not waitForCont:
                    pass
                value = splitText[i][-1].strip()

                # There are 3+ words and the sentence ends with one of the marks
                if not waitForCont and len(key) != 0:
                    lastKey = key
                    result[key].append(value)
                else:
                    result[lastKey][-1] = f'{result[lastKey][-1]} {value}'

                waitForCont = False if re.search(r'[.!?]$', value) else True
            elif len(splitText[i]) == 2:
                value = splitText[i][-1].strip()
                if waitForCont:
                    result[lastKey][-1] = f'{result[lastKey][-1]} {value}'
                else:
                    result[lastKey].append(value)

                waitForCont = False if re.search(r'[.!?]$', value) else True

        return result
