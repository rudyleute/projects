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

    def countCategories(self, params=None):
        result = dict({
            "select": ["frequency_id", "frequency_label", "COALESCE(COUNT(word.word_fk_frequency_id), 0) as number_in_category"],
            "join": ["left join", "word", [
                ("word.word_fk_frequency_id", '=', 'frequency.frequency_id')
            ]],
            "group by": ["frequency_id, frequency_label"],
            "order by": ["frequency_lowest_class ASC"]
        })

        for key in params or dict():
            if key in result:
                if key == "join":
                    result[key][2].extend(params[key])
                else:
                    result[key].extend(params[key])
            else:
                result[key] = params[key]

        return super().get(params=result, isDict=True)