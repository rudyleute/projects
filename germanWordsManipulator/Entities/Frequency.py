from .Tables import Tables


class Frequency(Tables):
    def __init__(self):
        super().__init__("frequency")

    def get(self, params=None, isDict=True, key=None):
        if not params or "order by" not in params:
            if not params:
                params = dict()

            params["order by"] = ["frequency_lowest_class ASC"]

        result = super().get(params, isDict=isDict)
        data = dict()

        for oneRow in result:
            data[oneRow[key or "frequency_label"]] = dict({
                "uuid": oneRow["frequency_id"],
                "from": oneRow["frequency_lowest_class"],
                "to": oneRow["frequency_highest_class"],
                "label": oneRow["frequency_label"]
            })

        return data
