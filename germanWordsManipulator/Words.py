class Words:
    __tableName = "words"

    def __init__(self, db):
        self.__db = db

    @staticmethod
    def __formWhereClause(whereData):
        whereClause = []
        for clause in whereData:
            if isinstance(list, clause):
                subclauses = []
                for info in clause:
                    subclauses.append(f"{info[0]} {info[2]} {info[1]}")

                whereClause.append(f"({str.join(' OR ', subclauses)})")

        return str.join(' AND ', whereClause)

    def __retrieve(self, queryParams):
        whereClause = None
        sort = None
        select = "*"

        if "select" in queryParams and len(queryParams["select"]):
            select = str.join(',', queryParams['select'])
        if "where" in queryParams:
            whereClause = Words.__formWhereClause(queryParams['where'])
            if len(whereClause) == 0:
                whereClause = None
        if "sort" in queryParams:
            sort = str.join(',', queryParams["sort"])

        query = (f"SELECT {select} FROM {Words.__tableName} "
                 f"WHERE {whereClause if whereClause is not None else '1=1'}"
                 f"{f'SORT BY {sort}' if sort is not None else str()}")

        return self.__db.execute(query)


