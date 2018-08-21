__author__ = 'hejin'

import os
from fdfs_client.client import *
from fdfs_client.tracker_client import *
from fdfs_client.storage_client import *
from fdfs_client.exceptions import *
from log.GTlog import *

client_file='D:\\ArcClassify\\src\\GTFastDFS\\client.conf'

class fastDFS_op:
    def __init__(self, confile = client_file):
        self.confile = confile
        self.client = Fdfs_client(self.confile)

    def upFile(self, filename):
        if os.path.exists(filename) is not True:
            return None, None, False
        try:
            ret = self.client.upload_by_file(filename)
            if (ret['Status'] != 'Upload successed.'):
                print (ret['Status'])
            return ret['Group name'], ret['Remote file_id'], True
        except (ConnectionError, ResponseError, DataError) as e:
            print("-------------------------------------------------------------")
            print(e)
            logError(e)
            return None, None, False

    def delFile(self,remote_filename_id):
        ret = False
        try:
            ret_tuple = self.client.delete_file(remote_filename_id)
            print('[+] %s' % ret_tuple[0])
            print('[+] remote_fileid: %s' % ret_tuple[1])
            print('[+] Storage IP: %s' % ret_tuple[2])
            ret = True
        except (ConnectionError, ResponseError, DataError) as e:
            print(e)
            logError(e)
        return ret

    def downFile(self, local_file, remote_filename_id):
        dir, file = os.path.split(local_file)
        ret = False
        if os.path.exists(dir) != True:
            return False
        try:
            ret_dict = self.client.download_to_file(local_file,remote_filename_id)
            for key in ret_dict:
                print('[+] %s : %s' % (key, ret_dict[key]))
            return True
        except (ConnectionError, ResponseError, DataError) as e:
            logError(e)
        return False

    def getMeta(self, remote_filename_id):
        ret = False
        try:
            ret_dict = self.client.get_meta_data(remote_filename_id)
            print(ret_dict)
            ret = True
        except (ConnectionError, ResponseError, DataError) as e:
            print(e)
            ret = False
            logError(e)
        return ret

    def list_all_groups(self):
        retvalue = None
        try:
            retvalue = self.client.list_all_groups()
        except (ConnectionError, ResponseError, DataError) as e:
            print(e)
            logError(e)
        return retvalue

    def list_one_groups(self, groupName):
        retvalue = None
        try:
            retvalue = self.client.list_one_group(groupName)
        except (ConnectionError, ResponseError, DataError) as e:
            print(e)
            logError(e)
        return retvalue

    def close(self):
        try:
            self.client.close_fdfs()
        except:
            pass

def demo():
    fastDFSop = fastDFS_op(client_file)
    groupName, remote_filename_id, retValue = fastDFSop.upFile('mysql_op.py')
    print (groupName, remote_filename_id, retValue)

if __name__ == '__main__':
    demo()




