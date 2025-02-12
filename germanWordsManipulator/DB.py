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
        self.__primaryKeys = {value["table_name"]: value["column_name"] for value in self.__retrievePK()}

    def __retrievePK(self):
        # retrieve all the primary keys for the tables
        query = "SELECT tc.table_name, c.column_name "\
                "FROM information_schema.table_constraints tc "\
                "JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) "\
                "JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema "\
                "AND tc.table_name = c.table_name AND ccu.column_name = c.column_name "\
                "WHERE constraint_type = 'PRIMARY KEY';"

        return self.__execute(query)

    @staticmethod
    def __convertForDB(data):
        return {DB.__convertValue(key, wrapStr=False): DB.__convertValue(value) for key, value in data.items()}

    @staticmethod
    def __convertValue(value, wrapStr=True):
        if not isinstance(value, str):
            value = str(value)
        elif wrapStr:
            value = f"'{value}'"

        return value

    @staticmethod
    def __listToQueryString(data, wrapStr=True, delim=','):
        return delim.join([DB.__convertValue(elem, wrapStr=wrapStr) for elem in data])

    def __execute(self, query, isDict=True):
        if isDict:
            cur = self.__connection.cursor(cursor_factory=RealDictCursor)
        else:
            cur = self.__connection.cursor()

        result = {}

        try:
            cur.execute(query)
            result = cur.fetchall()
        except psycopg2.ProgrammingError:  # TODO handle errors better: both insert and actual errors are handled here
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
                else:
                    clause = list(clause)[:2] + [str(clause[2])]
                whereClause.append(' '.join(list(clause)))

        return str.join(' AND ', whereClause)

    def select(self, queryParams, isDict=True):
        whereClause = sort = limit = groupBy = join = None
        select = "*"

        if "select" in queryParams and len(queryParams["select"]):
            select = ','.join(queryParams['select'])
        if "where" in queryParams:
            whereClause = DB.__formWhereClause(queryParams['where'])
            if len(whereClause) == 0:
                whereClause = None
        if "order by" in queryParams:
            sort = str.join(',', queryParams["order by"])
        if "limit" in queryParams and isinstance(queryParams["limit"], int):
            limit = queryParams["limit"]
        if "group by" in queryParams:
            groupBy = ', '.join(queryParams["group by"])
        if "join" in queryParams:
            condition = ' and '.join([
                f"{value[0]} {value[1]} {value[2]}"
                for value in queryParams['join'][2]
            ])
            join = (f"{queryParams['join'][0]} {queryParams['join'][1]} ON "
                    f"{condition}")

        query = (f"SELECT {select} FROM {queryParams['from']} "
                 f"{join or str()} "
                 f"{f'WHERE {whereClause}' if whereClause is not None else str()} "
                 f"{f'GROUP BY {groupBy}' if groupBy is not None else str()} "
                 f"{f'ORDER BY {sort}' if sort is not None else str()} "
                 f"{f'LIMIT {limit}' if limit is not None else str()}")

        return self.__execute(query, isDict=isDict)

    def insert(self, data):
        for row in data["insert"]:
            self.__execute(
                f"INSERT INTO {data['from']} ({DB.__listToQueryString(list(row.keys()), wrapStr=False)}) "
                f"VALUES ({DB.__listToQueryString(list(row.values()))})"
            )

    def update(self, data):
        for row in data["update"]:
            row["values"] = DB.__convertForDB(row["values"])
            self.__execute(
                f"UPDATE {data['from']} SET {', '.join([f'{key}={value}' for key, value in row['values'].items()])} "
                f"WHERE {self.__formWhereClause(row['condition']) if 'condition' in row else '1=1'}"
            )

    def __del__(self):
        self.__connection.close()
