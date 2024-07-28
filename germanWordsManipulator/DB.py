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

    def execute(self, query):
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

    def __del__(self):
        self.__connection.close()
