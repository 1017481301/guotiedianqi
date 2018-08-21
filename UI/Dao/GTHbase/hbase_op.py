__author__ = 'hejin'

from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from hbase import Hbase
from log.GTlog import *

import struct
import datetime

# Method for encoding ints with Thrift's string encoding
def encode(n):
    return struct.pack("i", n)

# Method for decoding ints with Thrift's string encoding
def decode(s):
   return int(s) if s.isdigit() else struct.unpack('i', s)[0]


class hbase_op:
    def __init__(self,dbhost,dbport,dbname=None,dbpassword=None):
        self.dbhost = dbhost
        self.dbname = dbname
        self.dbpassword = dbpassword
        self.dbport = dbport

        # Connect to HBase Thrift server
        self.transport = TTransport.TBufferedTransport(TSocket.TSocket(dbhost,dbport))
        self.protocol = TBinaryProtocol.TBinaryProtocolAccelerated(self.transport)

        # Create and open the client connection
        self.client = Hbase.Client(self.protocol)
        try:
            self.transport.open()
        except (Hbase.TException) as e:
            print ('transport.open()')
            logInfo('transport.open()')
            logInfo(e)

    def __del__(self):
        self.transport.close()

    def getColumnDescriptors(self):
        try:
            return self.client.getColumnDescriptors(self.dbname)
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException) as e:
            print(e)
            logInfo(e)
        return None

    def close(self):
        try:
            self.transport.close()
            return True
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException) as e:
            print(e)
            logInfo('close')
            logInfo(e)
        return False

    def createTable(self, columnFamilies):
        try:
            tables = self.client.getTableNames()
            if self.dbname in tables:
                return False
            TempcolumnFamilies = []
            for columnFamily in columnFamilies:
                name = Hbase.ColumnDescriptor(name=columnFamily)
                TempcolumnFamilies.append(name)
            self.client.createTable(self.dbname, TempcolumnFamilies)
            return True
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException,Hbase.IllegalArgument) as e:
            logInfo('createTable')
            logInfo(e)
            print(e)
        return False

    def isTableEnabled(self):
        try:
            tables = self.client.getTableNames()
            if self.dbname not in tables:
                return False
            return self.client.isTableEnabled(self.dbname)
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException) as e:
            logInfo('isTableEnabled')
            logInfo(e)
            print (e)
        return False

    def delTable(self):
        try:
            tables = self.client.getTableNames()
            if self.dbname not in tables:
                return False
            if self.isTableEnabled():
                self.client.disableTable(self.dbname)
            self.client.deleteTable(self.dbname)
            return True
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException) as e:
            logInfo('delTable')
            logInfo(e)
            print(e)
        return False

    def putByColumns(self, rowkey, args):
        mutations = []
        try:
            for key, value in args.items():
                if isinstance(value, bytes):
            #       print (key,value)
                    value = value.decode()
                    m_name = Hbase.Mutation(column=key, value = value)
                elif isinstance(value, str):
                    m_name = Hbase.Mutation(column=key, value=value)
                elif isinstance(value, int):
                    m_name = Hbase.Mutation(column=key, value=encode(value))
                elif isinstance(value, datetime.datetime):
                    return False
                mutations.append(m_name)
            self.client.mutateRow(self.dbname, rowkey, mutations)
            return True
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException,Hbase.IllegalArgument) as e:
            logInfo('putByColumns')
            logInfo(e)
            print(e)
        return False

    def putByColumn(self, rowkey, arg):
        mutations = []
        try:
            key = arg.key()
            value = arg[key]
            m_name = Hbase.Mutation(column=key, value = value)
            mutations.append(m_name)
            self.client.mutateRow(self.dbname, rowkey, mutations)
            return True
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException,Hbase.IllegalArgument) as e:
            logInfo('putByColumn')
            logInfo(e)
            print(e)
        return False

    def put(self, rowkey, columnFamilies, *args):
        mutations = []
        try:
            for j, column in enumerate(args):
                if isinstance(column, str):
                    m_name = Hbase.Mutation(column=columnFamilies[j]+':'+'0', value=column)
                elif isinstance(column, int):
                    m_name = Hbase.Mutation(column=columnFamilies[j]+':'+'0', value=encode(column))
                mutations.append(m_name)
            self.client.mutateRow(self.dbname, rowkey, mutations)
            return True
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException,Hbase.IllegalArgument) as e:
            logInfo('put')
            logInfo(e)
            print(e)
        return False

    def puts(self, rowkey, columnFamilies, values):
        mutationsBatch = []
        try:
            if not isinstance(rowkey, list):
                rowKeys = [rowkey] * len(values)
            for i, value in enumerate(values):
                mutations = []
                for j, column in enumerate(value):
                    if isinstance(column, str):
                        m_name = Hbase.Mutation(column=columnFamilies[j]+':'+'0', value=column)
                    elif isinstance(column, int):
                        m_name = Hbase.Mutation(column=columnFamilies[j]+':'+'0', value=encode(column))
                    mutations.append(m_name)
                mutationsBatch.append( Hbase.BatchMutation(row=rowKeys[i], mutations=mutations))
            self.client.mutateRows(self.dbname, mutationsBatch)
            return True
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException,Hbase.IllegalArgument) as e:
            logInfo('puts')
            logInfo(e)
            print(e)
        return False

    def getRow(self, row, columnFamilies):
        try:
            rows = self.client.getRow(self.dbname, row)
            ret = []
            for row in rows:
                rd = {'row': row.row}
                for j, column in enumerate(columnFamilies):
                    if isinstance(column, str):
                        rd.update({column: row.columns.get(column).value})
                    elif isinstance(column, int):
                        rd.update({column: decode(row.columns.get(column).value)})
                ret.append(rd)
            return ret
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException,Hbase.IllegalArgument) as e:
            logInfo('getRow')
            logInfo(e)
            print(e)
        return None

    def getRows(self, rows, columnFamilies):
        try:
            for row in rows:
                yield self.getRow(row, columnFamilies)
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException,Hbase.IllegalArgument) as e:
            logInfo('getRows')
            logInfo(e)
            print(e)
        return None


    def getRowByKey(self, rowkey):
        try:
            return self.client.getRow(self.dbname, rowkey)
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException,Hbase.IllegalArgument) as e:
            logInfo('getRowByKey')
            logInfo(e)
            print(e)
        return None

    def scanner(self, columnFamilies, numRows = 100, startRow=None):
        try:
            scannerId = self.client.scannerOpen(self.dbname, startRow, columnFamilies)
            ret = []
            rowList = self.client.scannerGetList(scannerId, numRows)
            while rowList:
                for r in rowList:
                    rd = {'row': r.row}
                    for k, v in r.columns.items():
                        cf, qualifier = k.split(':')
                        if cf not in rd:
                            rd[qualifier] = {}

                        idx = columnFamilies.index(cf)
                        if isinstance(columnFamilies[idx], str):
                            rd[qualifier].update({ qualifier: v.value })
                        elif isinstance(columnFamilies[idx], int):
                            rd[qualifier].update({ qualifier: decode(v.value) })

                    ret.append(rd)
                rowList = self.client.scannerGetList(scannerId, numRows)
            self.client.scannerClose(scannerId)
            return ret
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException,Hbase.IllegalArgument) as e:
            logInfo('scanner')
            logInfo(e)
            print(e)
        return None

    def deleteAllByRow(self, row):
        try:
            self.client.deleteAllRow(self.dbname, row)
            return True
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException,Hbase.IllegalArgument) as e:
            logInfo('deleteAllByRow')
            logInfo(e)
            print(e)
        return False

    def deleteAllCells(self, row, column):
        try:
            self.client.deleteAll(self.dbname, row, column)
            return True
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException,Hbase.IllegalArgument) as e:
            logInfo('deleteAllCells')
            logInfo(e)
            print(e)
        return False

    def get(self, row, column):
        try:
            return self.client.get(self.dbname, row, column)
        except (Hbase.IOError,Hbase.TException,Hbase.TApplicationException,Hbase.IllegalArgument) as e:
            logInfo('get')
            logInfo(e)
            print(e)
        return None

def test():
    colums=['a','b','c']

    hbaseop = hbase_op('192.168.1.70',9090,'fastDFSFileMap')
    #hbaseop = hbase_op('192.168.1.70', 9090, 'yutaotest')
    #hbaseop.createTable(colums)

   # for i in range(10):
   #     hbaseop.put(str(i), colums,'a'+str(i), 'b'+str(i), 'c'+str(i))
   # print (hbaseop.getColumnDescriptors())

 #   print (hbaseop.getRow( str(3), colums))
 #   print (hbaseop.getRow(str(3), ['a','b']))


    rows= hbaseop.getRowByKey('Fe31eb1787ec04d9cbcf5c0bd8979ce7b')
    #print (rows[0])
    print (rows)
    for row in rows:
        print(row)
        for key in row.columns:
            print(key+'1')
            ret = key.find('remotefilename')
            print(ret)
            if ret != -1:
                romatefilename = row.columns.get(key).value
                print(romatefilename)


 #   print (hbaseop.deleteAllByRow(str(5)))
 #   print (hbaseop.scanner(colums, numRows=1, startRow=str(20)))

if __name__ == '__main__':
    test()
