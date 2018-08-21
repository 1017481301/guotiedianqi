__author__ = 'hejin'
from GTMysql.mysql_op import mysql_op

def next(cursor):
    return cursor.fetchone()

def deal_tt(row, cursor):
    while row != None:
        print (row)
        row = next(cursor)

def deal_tt2(row, cursor):
    while row != None:
        print (row)
        row = next(cursor)

def procedure():
    oracleop = mysql_op(host='192.168.1.90',port = 3306,db= 'test', dbuser = 'root',dbpassword='123456',maxconn=3, min_conn=2)
    oracleop.callProcedure('new_procedure',2, deal_tt, deal_tt2)
if __name__ == '__main__':
    procedure()