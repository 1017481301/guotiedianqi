__author__ = 'lenovo'

import time
from GTOracle.oracle_op import oracle_op
DNS = '192.168.1.100:1521/testdb'

def func(row):
	if row[0]:
		print (row)
		length = len(row[0])
		row0 = row[0]
		virtual_dir1 = str(row0[1:length])
		index = virtual_dir1.find('/')
		virtual_dir = virtual_dir1[0:index]
		backupdir = virtual_dir1[index+1:len(virtual_dir1)]
		print (backupdir)
		time.sleep(10)
	return

oracleop = oracle_op('dtctest','dtctest',DNS,3,2)
sql = "select * from test_login"
conn, cursor, row = oracleop.openSelectOne(sql)
oracleop.selectOpCallback(sql, func)

for fname, lname in cursor:
    print ("Values:", fname, lname)