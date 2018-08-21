__author__ = 'hejin'

import MySQLdb
from DBUtils.PooledDB import PooledDB

class mysql_op:
    def __init__(self, host=None, port=None, dbuser=None, db=None, dbpassword=None, maxconn=1, min_conn=1):
        self.dbuser = dbuser
        self.dbhost = host
        self.dbport = port
        self.dbname = db
        self.dbpassword = dbpassword
        self.maxconn = maxconn
        self.minconn = min_conn
        try:
            self.mysqlConnPool = PooledDB(MySQLdb, 5, host=self.dbhost, user = self.dbuser, passwd = self.dbpassword,  db= self.dbname, port=self.dbport, charset="utf8")
        except Exception as e:
            print('PooledDB error')

    def close(self):
        try:
            self.mysqlConnPool.close()
            return True
        except (MySQLdb.DatabaseError,MySQLdb.DataError,MySQLdb.ProgrammingError,MySQLdb.OperationalError) as e:
            print(e)
        return False

    def getConn(self):
        try:
            return self.mysqlConnPool.connection(shareable=False)
        except (MySQLdb.DatabaseError,MySQLdb.DataError,MySQLdb.ProgrammingError,MySQLdb.OperationalError) as e:
            print(e)
        return None

    def closeConn(self, conn):
        try:
            conn.close()
            return True
        except (MySQLdb.DatabaseError,MySQLdb.DataError,MySQLdb.ProgrammingError,MySQLdb.OperationalError) as e:
            print(e)
        return False

    def escapeString(self, content):
        if content is None:
            return None
        try:
            return MySQLdb.escape_string(content)
        except (MySQLdb.DatabaseError,MySQLdb.DataError,MySQLdb.ProgrammingError,MySQLdb.OperationalError) as e:
            print(e)
        return None

    def selectAll(self, sql):
        conn = self.getConn()
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except (MySQLdb.DatabaseError,MySQLdb.DataError,MySQLdb.ProgrammingError,MySQLdb.OperationalError) as e:
            print(e)
            return None
        finally:
            self.closeConn(conn)

    def updateAndinsert(self,sql):
        conn = self.getConn()
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            return True
        except (MySQLdb.DatabaseError,MySQLdb.DataError,MySQLdb.ProgrammingError,MySQLdb.OperationalError) as e:
            print(e)
            return False
        finally:
            self.closeConn(conn)

# three function combine to perform one by one select.
    def openSelectOne(self,sql):
        conn = self.getConn()
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            return conn, cursor, row
        except (MySQLdb.DatabaseError,MySQLdb.DataError,MySQLdb.ProgrammingError,MySQLdb.OperationalError) as e:
            print(e)
        return None

    def next(self, cursor):
        try:
            return cursor.fetchone()
        except (MySQLdb.DatabaseError,MySQLdb.DataError,MySQLdb.ProgrammingError,MySQLdb.OperationalError) as e:
            print(e)
        return None

    def closeSelectOne(self,conn, cursor):
        try:
            cursor.close()
            return True
        except (MySQLdb.DatabaseError,MySQLdb.DataError,MySQLdb.ProgrammingError,MySQLdb.OperationalError) as e:
            print(e)
            return False
        finally:
            self.closeConn(conn)

    def callProcedure(self, Procedure, funcNum, *dealFuncs):
        retvalue = []
        conn = self.getConn()
        try:
            cursor = conn.cursor()
            cursor.callproc(Procedure)
            for i, dealFunc in enumerate(dealFuncs):
                if((i < funcNum) and (dealFunc != None)):
                    row = cursor.fetchall()
                    dealFunc(row, cursor)
                    cursor.nextset()
            cursor.close()
            return retvalue
        except (MySQLdb.DatabaseError,MySQLdb.DataError,MySQLdb.ProgrammingError,MySQLdb.OperationalError) as e:
            print(e)
            return None
        finally:
            self.closeConn(conn)


def demo():
    oracleop = mysql_op(host='192.168.1.90',port = 3306,db= 'test', dbuser = 'root',dbpassword='123456',maxconn=3, min_conn=2)
    #sql = "select AA.SVALUE1, AA.SVALUE14, AA.ID, BB.DIC_CODE from NHS3C.ALARM AA, NHS3C.SYS_DIC BB where (AA.STATUS != 'AFSTATUS01' AND AA.ALARM_ANALYSIS is not null AND (BB.DIC_CODE = 'AFLG_RL' OR BB.DIC_CODE = 'AFLG_SUN' OR BB.DIC_CODE = 'AFLG_LIGHT') and AA.alarm_analysis = BB.code_name)"
    sql = "select * from test.tt"
    conn, cursor, row = oracleop.openSelectOne(sql)
    while row != None:
        print (row)
        row = oracleop.next(cursor)
    oracleop.closeSelectOne(conn,cursor)

if __name__ == '__main__':
    demo()

