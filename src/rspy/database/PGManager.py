from psycopg2 import pool
import mybatis_mapper2sql
import traceback
import pandas as pd

class PGManager(object):
    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(PGManager, self).__new__(self)
            self.__connection_pool = None
        return self.instance

    def createPool(self, user, passwd, db, host, minCon=5, maxCon=20, port=5432):
        self.close()
        self.__connection_pool = pool.SimpleConnectionPool(
            minCon, maxCon, user=user, password=passwd,
            host=host, port=port, database=db)

    def close(self):
        if (self.__connection_pool):
            self.__connection_pool.closeall()

    def setMapper(self, xmlMapperFile):
        self._mapper, _ = mybatis_mapper2sql.create_mapper(xml=xmlMapperFile)

    def sql(self, sql):
        try:
            connection = self.__connection_pool.getconn()
            cursor = connection.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            cursor.close()
            self.__connection_pool.putconn(connection)

            return records
        except:
            traceback.print_exc()

    def sqlPandas(self, sql, dtype=None):
        try:
            connection = self.__connection_pool.getconn()
            df = pd.read_sql(sql, connection)
            self.__connection_pool.putconn(connection)

            if dtype is not None:
                df = df.astype(dtype)

            return df
        except:
            traceback.print_exc()

    def query(self, mapId, params=None):
        try:
            connection = self.__connection_pool.getconn()
            cursor = connection.cursor()
            statement = mybatis_mapper2sql.get_child_statement(self._mapper, mapId)
            cursor.execute(statement, [params])
            records = cursor.fetchall()
            cursor.close()
            self.__connection_pool.putconn(connection)

            return records
        except:
            traceback.print_exc()

    def queryPandas(self, mapId, params=None, dtype=None):
        try:
            connection = self.__connection_pool.getconn()
            statement = mybatis_mapper2sql.get_child_statement(self._mapper, mapId)
            df = pd.read_sql(statement, connection, params=[params])
            self.__connection_pool.putconn(connection)

            if dtype is not None:
                df = df.astype(dtype)

            return df
        except:
            traceback.print_exc()

    def execute(self, mapId, params=None):
        try:
            connection = self.__connection_pool.getconn()
            cursor = connection.cursor()
            statement = mybatis_mapper2sql.get_child_statement(self._mapper, mapId)
            cursor.execute(statement, params)
            cursor.close()
            connection.commit()
            self.__connection_pool.putconn(connection)
        except:
            traceback.print_exc()

    def executeMany(self, mapId, paramsList):
        try:
            connection = self.__connection_pool.getconn()
            cursor = connection.cursor()
            statement = mybatis_mapper2sql.get_child_statement(self._mapper, mapId)
            cursor.executemany(statement, paramsList)
            cursor.close()
            connection.commit()
            self.__connection_pool.putconn(connection)
        except:
            traceback.print_exc()

    def asyncExecuteMany(self, mapper, mapId, paramsList):
        try:
            p = Process(target=self.executeMany, args=(mapId, paramsList))
            p.start()
            p.join()
        except:
            traceback.print_exc()