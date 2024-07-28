import psycopg2


class DB:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.__connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

    @staticmethod
    def __listToQueryString(data, wrapStr=True, delim=','):
        prepData = []
        for elem in data:
            if not isinstance(elem, str):
                elem = str(elem)
            elif wrapStr:
                elem = f"'{elem}'"

            prepData.append(elem)

        return str.join(delim, prepData)

    def __execute(self, query):
        cur = self.__connection.cursor()
        cur.execute(query)
        try:
            result = cur.fetchall()
        except psycopg2.ProgrammingError:
            if cur.rowcount == 0:
                raise psycopg2.ProgrammingError("The query has not been processed")
            self.__connection.commit()
            result = None
        finally:
            cur.close()

        return result

    @staticmethod
    def __formWhereClause(whereData):
        whereClause = []
        for clause in whereData:
            if isinstance(clause, list):
                subclauses = []
                for info in clause:
                    subclauses.append(f"{info[0]} {info[1]} {DB.__listToQueryString([info[1]])}")

                whereClause.append(f"({str.join(' OR ', subclauses)})")

        return str.join(' AND ', whereClause)

    def select(self, queryParams):
        whereClause = None
        sort = None
        limit = None
        select = "*"

        if "select" in queryParams and len(queryParams["select"]):
            select = str.join(',', queryParams['select'])
        if "where" in queryParams:
            whereClause = DB.__formWhereClause(queryParams['where'])
            if len(whereClause) == 0:
                whereClause = None
        if "sort" in queryParams:
            sort = str.join(',', queryParams["sort"])
        if "limit" in queryParams and isinstance(queryParams["limit"], int):
            limit = queryParams["limit"]

        query = (f"SELECT {select} FROM {queryParams['from']} "
                 f"WHERE {whereClause if whereClause is not None else '1=1'} "
                 f"{f'SORT BY {sort}' if sort is not None else str()} "
                 f"{f'LIMIT {limit}' if limit is not None else str()}")

        return self.__execute(query)

    def insert(self, data):
        for row in data["insert"]:
            self.__execute(
                f"INSERT INTO {data['from']} ({DB.__listToQueryString(list(row.keys()), wrapStr=False)}) "
                f"VALUES ({DB.__listToQueryString(list(row.values()))})"
            )

    def __del__(self):
        self.__connection.close()
