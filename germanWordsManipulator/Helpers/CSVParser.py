import csv


class CSVParser:
    def __init__(self):
        pass

    @staticmethod
    def readFile(filename, hasHeader=True):
        with open(filename, newline='') as file:
            if hasHeader:
                return list(csv.DictReader(file))
            return list(csv.reader(file))

    @staticmethod
    def editFile(filename, data, toAppend=True, hasHeader=None):
        with open(filename, 'w' if not toAppend else 'a', newline='') as file:
            if hasHeader:
                writer = csv.DictWriter(file, fieldnames=list(data[0].keys()))
                if not toAppend:
                    writer.writeheader()

            else:
                writer = csv.writer(file)

            writer.writerows(data)


