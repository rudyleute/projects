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
        result = cur.execute(query)
        cur.close()

        return result

    def __del__(self):
        self.__connection.close()
