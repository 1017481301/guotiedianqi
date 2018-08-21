import time

def sleepTime(inFile,outFile,fileType,type,strartTime="None",endTime="None",timePre='【',timeafter='】'):
    f=open(inFile.strip(),'r')
    lines=f.readlines()
    f.close()
    timePreN=len(timePre)
    start=False
    message=dict()
    results=[]
    for l in lines:
        if (type and not start) or (strartTime in l):
            start=True
        elif start:
            if type or (endTime in l):
                start=False
                break
            myTime=l[l.find(timePre)+timePreN:l.find(timeafter)]        #获取时间
            myFile=l[l.find(timeafter)+len(timeafter):].split(' ')[1].strip()  #获取文件

            #时间转换
            ms=int((myTime.split(','))[1])#毫秒
            stime=(myTime.split(','))[0]#秒
            s=time.mktime(time.strptime(stime, "%Y-%m-%d %H:%M:%S"))
            nowMs=int(1000*s+ms)
            try :
                message[myFile]
            except:
                message[myFile] = nowMs
            else:
                message[myFile]=abs(message[myFile]-nowMs)
    #C:/Users/admin/Desktop/MV.log
    print(message)
    f1 = open(outFile.strip(), 'w')
    #fileType
    time.sleep(2)
    for k in message.keys():
        if fileType.upper()=='ALL' :
            if message[k]<999999:
                results.append(message[k])
                time.sleep(0.5)
                f1.write(str(message[k]))
                f1.write('\n')
        else:
            if message[k]<999999 and (((fileType.split('-')[0]).upper()==k.split('.')[1].upper()) and ('_'+fileType.split('-')[1]+'_') in k):
                results.append(message[k])
                time.sleep(0.5)
                f1.write(str(message[k]))
                f1.write('\n')
    f1.close()
    print(results)
    return results

if __name__=='__main__':
    print('说明：请设置开始和输出结果目录（统一用正斜杠），同时接入时间用文件中的时间如:2018-07-11 16:27:32')
    inFile = input("待分析日志目录：")
    outFile = input("分析结果文件目录：")
    testType=input("是否全量分析(Y/N)：")
    fileType=input("分析文件类型(DLV-1、MV-2、MV-3、MV-4、SCS-9、ALL)：")
    if testType.upper()=='N':
        type=False  #True代表全量,False代表按时间段
        strartTime = input("限定开始时间：")
        endTime = input("限定结束时间：")
        sts = sleepTime(inFile, outFile,fileType,type, strartTime, endTime)
    else:
        type=True
    sts = sleepTime(inFile, outFile, fileType,type)
    print(len(sts))
    #2018-07-10 16:23:06
    #2018-07-10 16:23:18
    #C:/Users/admin/Desktop/MV.log