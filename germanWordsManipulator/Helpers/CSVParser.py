import csv


class CSVParser:
    def __init__(self):
        pass

    @staticmethod
    def readFile(filename, hasHeader=True, keyField=None, keyLower=False):
        with open(filename, newline='') as file:
            if not hasHeader:
                return list(csv.reader(file))

            if keyField is None:
                return list(csv.DictReader(file))

            reader = list(csv.DictReader(file))
            if keyLower:
                return {row[keyField].lower(): row for row in reader}
            else:
                return {row[keyField]: row for row in reader}

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


