__author__ = 'hejin'

import phoenixdb
from log.GTlog import *


default_phoenix_url = 'http://192.168.1.70:8765/'

class phoenix_op:
    def __init__(self, url=default_phoenix_url):
        self.phoenix_url = url
        try:
            self.connection = phoenixdb.connect(self.phoenix_url, autocommit=True)
        except Exception as e:
            self.connection = None
            logInfo('phoenix connection')
            logInfo(e)

    def close(self):
        if self.connection is not None:
            self.connection.close()

    def selectAll(self, sql):
        if self.connection is None:
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Exception as e:
            print(e)
            logInfo('phoenix selectAll')
            logInfo(e)
            return None

    def updateAndinsert(self, sql, parameters=None):
        if self.connection is None:
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql,parameters)
            cursor.close()
            return True
        except Exception as e:
            print(e)
            logInfo('phoenix updateAndinsert')
            logInfo(e)
            return False

    # three function combine to perform one by one select.
    # default is 1, support many fetch.
    def openSelectOneOrMany(self, sql, size=1):
        if self.connection is None:
            return None, None
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            if size == 1:
                row = cursor.fetchone()
            elif size > 1:
                row = cursor.fetchmany(size=size)
            return cursor, row
        except Exception as e:
            print(e)
            logInfo('phoenix openSelectOne')
            logInfo(e)
        return cursor, None

    def next(self, cursor, size=1):
        try:
            if size == 1:
                row = cursor.fetchone()
            elif size > 1:
                row = cursor.fetchmany(size=size)
            return row
        except Exception as e:
            print(e)
            logInfo('phoenix next')
            logInfo(e)
        return None

    def closeSelectOne(self, cursor):
        try:
            cursor.close()
            return True
        except Exception as e:
            print(e)
            logInfo('phoenix closeSelectOne')
            logInfo(e)
            return False

    def selectOpCallback(self, sql, callback, arg):
        if self.connection is None:
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            while row is not None:
                callback(row, arg)
                print (cursor)
                row = cursor.fetchone()
            cursor.close()
            return True
        except Exception as e:
            print(e)
            logInfo('phoenix selectOpCallback')
            logInfo(e)
            return False

def demo():
    create_sql = "CREATE TABLE IF NOT EXISTS phoenix (id INTEGER PRIMARY KEY, username VARCHAR, age INTEGER, school VARCHAR)"
    phoenixop = phoenix_op(url=default_phoenix_url)
    retvalue = phoenixop.updateAndinsert(create_sql)
    print('1111create retvalue:%d'%retvalue)

#    index_sql="CREATE index index1 ON phoenix (age) include (school)"
    index_sql2="CREATE index IF NOT EXISTS index2 ON phoenix (age, username) include (school)"
    retvalue = phoenixop.updateAndinsert(index_sql2)
    print('1111create retvalue:%d'%retvalue)

    insert_sql="UPSERT INTO phoenix VALUES (?, ?, ?, ?)"
    parameters = (11, 'admin1', 41, 'school1')
    retvalue = phoenixop.updateAndinsert(insert_sql, parameters)
    print('222create retvalue:%d'%retvalue)

    select_sql = "SELECT * FROM phoenix ORDER BY age"
    retvalue = phoenixop.selectAll(select_sql)
    print('3333create retvalue:%s'%retvalue)

if __name__ == '__main__':
    demo()