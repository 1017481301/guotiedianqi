# _*_ coding=utf-8 _*_
import cx_Oracle
import os
import json
import time
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def getTestData(dblink,strat_time):
    test_data=[]
    getData=3
    dbc=cx_Oracle.connect(dblink)
    cur=dbc.cursor()
    #result=cur.execute("SELECT t.loginid,t.password,t.flag,t.assert FROM  TEST_LOGIN t ")
    result = cur.execute("SELECT a.id,a.svalue3 FROM  nhs3c.alarm a where a.raised_time>=to_date('"+strat_time+"','yyyy-mm-dd') and a.raised_time<=to_date('"+strat_time+"','yyyy-mm-dd')+30 and a.svalue3 is not null ")
    for data in result:
        #print(data)
        try:
            res=(json.loads(data[1]))["FRAME_INFO"]
        except:
            continue
        #time.sleep(0.01)
        for r in res:
            if (int(r.split(',')[getData])>=100000 or int(r.split(',')[getData])<=-100000):
                print(data[0],r.split(',')[getData])
    cur.close()
    dbc.close()
    return test_data
def getFun(dblink):
    class_fun=[]
    dbc = cx_Oracle.connect(dblink)
    cur = dbc.cursor()
    result = cur.execute("select distinct t.function,t.attribute_class,t.type from tsys_element t where  t.function is not null and t.type is not null")
    print(result)
    for data in result:
        class_fun.append(data)
    print(class_fun)
    return class_fun
if __name__ == '__main__':
    print(getTestData("infodept/JSITWVVAYIGPFFSKPRQC@192.168.1.248:1521/train6c",'2018-02-01'))
    #getFun("dtctest/dtctest@192.168.1.100/testdb")