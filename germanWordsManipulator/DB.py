import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION


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

    def __execute(self, query, isDict=True):
        if isDict:
            cur = self.__connection.cursor(cursor_factory=RealDictCursor)
        else:
            cur = self.__connection.cursor()

        result = {}

        try:
            cur.execute(query)
            result = cur.fetchall()
        except psycopg2.ProgrammingError:
            if cur.rowcount == 0:
                self.__connection.rollback()
                raise psycopg2.ProgrammingError("The query has not been processed")

            self.__connection.commit()
        # TODO this does not catch unique constraint violation error
        except errors.lookup(UNIQUE_VIOLATION):
            self.__connection.rollback()
            pass
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
            else:
                if clause[2] is None:
                    clause = list(clause)[:2] + ['NULL']
                elif isinstance(clause[2], str):
                    clause = list(clause)[:2] + [f"'{clause[2]}'"]
                whereClause.append(' '.join(list(clause)))

        return str.join(' AND ', whereClause)

    def select(self, queryParams, isDict=True):
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
                 f"WHERE {whereClause or '1=1'} "
                 f"{f'SORT BY {sort}' if sort is not None else str()} "
                 f"{f'LIMIT {limit}' if limit is not None else str()}")

        return self.__execute(query, isDict=isDict)

    def insert(self, data):
        for row in data["insert"]:
            self.__execute(
                f"INSERT INTO {data['from']} ({DB.__listToQueryString(list(row.keys()), wrapStr=False)}) "
                f"VALUES ({DB.__listToQueryString(list(row.values()))})"
            )

    def __del__(self):
        self.__connection.close()
