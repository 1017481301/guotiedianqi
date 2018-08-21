__author__ = 'hejin'
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
mydir = "D:\\测试开发\\instantclient-basic-nt-11.2.0.3.0\\instantclient_11_2"
os.environ["MYDIR"] = mydir
#print(os.environ["MYDIR"])
pathV = os.environ["PATH"]
#print(pathV)
os.environ["PATH"] = mydir + ";" + os.environ["PATH"]

import cx_Oracle
from DBUtils.PooledDB import PooledDB
from log.GTlog import *

DNS = '192.168.1.248:1521/train6C'
class oracle_op:
    def __init__(self, dbuser, dbpassword, dns, maxconn, min_conn):
        self.dbuser = dbuser
        self.dbpassword = dbpassword
        self.maxconn = maxconn
        self.minconn = min_conn
        self.dns = dns
        #self.CC = cx_Oracle.makedsn('192.168.1.248', 1521, 'train6C')
        #print (self.CC)
        try:
            self.oracleConnPool = PooledDB(cx_Oracle, user = self.dbuser, password = self.dbpassword, dsn = self.dns, mincached=2,maxcached=2,maxshared=2,maxconnections=self.maxconn)
        except Exception as e:
            print('PooledDB error')
            logInfo(e)


    def close(self):
        try:
            self.oracleConnPool.close()
            return True
        except Exception as e:
            logInfo('close')
            logInfo(e)
            print(e)
        return False

    def getConn(self):
        try:
            return self.oracleConnPool.connection(shareable=False)
        except (cx_Oracle.DatabaseError,cx_Oracle.DataError,cx_Oracle.ProgrammingError,cx_Oracle.OperationalError) as e:
            logInfo('getConn')
            logInfo(e)
            print(e)
        return None

    def closeConn(self, conn):
        try:
            conn.close()
            return True
        except (cx_Oracle.DatabaseError,cx_Oracle.DataError,cx_Oracle.ProgrammingError,cx_Oracle.OperationalError) as e:
            logInfo('closeConn')
            logInfo(e)
            print(e)
        return False

    def selectAll(self,sql):
        conn = self.getConn()
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except (cx_Oracle.DatabaseError,cx_Oracle.DataError,cx_Oracle.ProgrammingError,cx_Oracle.OperationalError) as e:
            print(e)
            logInfo('selectAll')
            logInfo(e)
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
        except (cx_Oracle.DatabaseError,cx_Oracle.DataError,cx_Oracle.ProgrammingError,cx_Oracle.OperationalError) as e:
            print(e)
            logInfo('updateAndinsert')
            logInfo(e)
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
        except (cx_Oracle.DatabaseError,cx_Oracle.DataError,cx_Oracle.ProgrammingError,cx_Oracle.OperationalError) as e:
            print(e)
            logInfo('openSelectOne')
            logInfo(e)
        return None

    def next(self, cursor):
        try:
            return cursor.fetchone()
        except (cx_Oracle.DatabaseError,cx_Oracle.DataError,cx_Oracle.ProgrammingError,cx_Oracle.OperationalError) as e:
            print(e)
            logInfo('next')
            logInfo(e)
        return None

    def closeSelectOne(self,conn, cursor):
        try:
            cursor.close()
            return True
        except (cx_Oracle.DatabaseError,cx_Oracle.DataError,cx_Oracle.ProgrammingError,cx_Oracle.OperationalError) as e:
            print(e)
            logInfo('closeSelectOne')
            logInfo(e)
            return False
        finally:
            self.closeConn(conn)

    def selectOpCallback(self, sql, callback, arg):
        conn = self.getConn()
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            print(row[2])
            print (cursor)
            while (row is not None):
                callback(row, arg)
                print (cursor)
                row = cursor.fetchone()
            cursor.close()
            return True
        except (cx_Oracle.DatabaseError,cx_Oracle.DataError,cx_Oracle.ProgrammingError,cx_Oracle.OperationalError) as e:
            print(e)
            logInfo('selectOpCallback')
            logInfo(e)
            return False
        finally:
            self.closeConn(conn)

def demo():
    oracleop = oracle_op('infodept','JSITWVVAYIGPFFSKPRQC',DNS,3,2)
    sql = "select AA.SVALUE1, AA.SVALUE14, AA.ID, BB.DIC_CODE from nhs3c.ALARM AA, nhs3c.sys_dic BB where (AA.RAISED_TIME > SYSDATE - 26 AND AA.STATUS != 'AFSTATUS01' AND AA.ALARM_ANALYSIS is not null AND (BB.DIC_CODE = 'AFLG_RL' OR BB.DIC_CODE = 'AFLG_SUN' OR BB.DIC_CODE = 'AFLG_LIGHT') and AA.alarm_analysis = BB.code_name)"
    #conn, cursor, row = oracleop.openSelectOne(sql)

    arg = '171208'
    QueryRecord = "select AA.SVALUE1, AA.SVALUE14, AA.ID, AA.DETECT_DEVICE_CODE,AA.RAISED_TIME,AA.CODE,AA.CODE_NAME, AA.STATUS_NAME, AA.DATA_TYPE, AA.Nvalue1, AA.DIR_PATH, AA.SVALUE11, AA.SVALUE5, AA.SVALUE9, AA.SVALUE3 from nhs3c.alarm AA where (AA.RAISED_TIME >=  to_date('%s','yymmdd') AND  AA.RAISED_TIME<  to_date('%s','yymmdd') + 1)"
    QueryRecord = QueryRecord % (arg, arg)

    conn, cursor, row = oracleop.openSelectOne(QueryRecord)



    while row != None:
        print (row[2])
        length = len(row[0])
        row0 = row[0]
        virtual_dir1 = str(row0[1:length])
        index = virtual_dir1.find('/')
        virtual_dir = virtual_dir1[0:index]
        backupdir = virtual_dir1[index+1:len(virtual_dir1)]
        print (backupdir)
        row = oracleop.next(cursor)
    oracleop.closeSelectOne(conn,cursor)

if __name__ == '__main__':
    demo()
