import os
from pyhdfs import *


hosts='192.168.1.70:50070,192.168.1.71:50070'
username='root'

class hdfs_op:
    def __init__(self, hosts, username):
        self.hosts=hosts
        self.username=username
        self.client=HdfsClient(hosts, username)

    def listdir(self, path):
        if not self.exists(path):
            return False
        try:
            ret=self.client.listdir(path)
            return ret
        except HdfsException as e:
            print(e)
        return False

    def exists(self, path):
        try:
            ret = self.client.exists(path)
            return ret
        except HdfsException as e:
            print(e)
        return False

    def mkdirs(self, path):
        if self.exists(path):
            return False
        try:
            ret = self.client.mkdirs(path)
            return ret
        except HdfsException as e:
            print(e)
        return False

    def upload(self, localsrc, dest, **kwargs):
        """
        :param localsrc:
        :param dest:
        :param kwargs: dict={}
        :param overwrite: (bool) – If a file already exists, should it be overwritten?
        :param blocksize: (long) – The block size of a file.
        :param replication: (short) – The number of replications of a file.
        :param permission: (octal) – The permission of a file/directory. Any radix-8 integer (leading zeros may be omitted.)
        :param buffersize: (int) – The size of the buffer used in transferring data.
        """
        if not os.path.exists(localsrc):
            return False
        #if self.exists(dest):
        #    return False
        try:
            self.client.copy_from_local(localsrc, dest, **kwargs)
            return True
        except HdfsException as e:
            print(e)
        return False

    def download(self, src, localdest):
        if not self.exists(src):
            return False
        if self.file_status(src).type !="FILE":
            return False
        try:
            self.client.copy_to_local(src, localdest)
            return True
        except (HdfsException, IOError) as e:
            print(e)
        return False

    def delete(self, path):
        if not self.exists(path):
            return False
        try:
            self.client.delete(path)
            return True
        except HdfsException as e:
            print(e)
        return False

    def file_checksum(self, path):
        if not self.exists(path):
            return None
        if self.file_status(path).type !="FILE":
            return None
        try:
            ret = self.client.get_file_checksum(path)
            return ret
        except HdfsException as e:
            print(e)
        return None

    def file_status(self, path):
        if not self.exists(path):
            return None
        try:
            ret = self.client.get_file_status(path)
            return ret
        except HdfsException as e:
            print(e)
        return None

    def list_status(self, path):
        if not self.exists(path):
            return None
        try:
            ret = self.client.list_status(path)
            return ret
        except HdfsException as e:
            print(e)
        return None

    def create(self, path, data, **kwargs):
        try:
            self.client.create(path, data, **kwargs)
            return True
        except HdfsException as e:
            print(e)
        return False

    def open(self, path, **kwargs):
        """
        :param path:
        :param kwargs:
        :param offset: (long) – The starting byte position.
        :param length: (long) – The number of bytes to be processed.
        :param buffersize: (int) – The size of the buffer used in transferring data.
        :return:
        """
        if not self.exists(path):
            return False
        if self.file_status(path).type !="FILE":
            return False
        try:
            ret = self.client.open(path,**kwargs)
            return ret
        except HdfsException as e:
            print(e)
        return False

    def set_replication(self, path, **kwargs):
        """
        Set replication for an existing file.
        :param path:
        :param kwargs:
        :param replication: (short) – new replication
        :return: true if successful; false if file does not exist or is a directory
        """
        if not self.exists(path):
            return False
        if self.file_status(path).type !="FILE":
            return False
        try:
            self.client.set_replication(path,**kwargs)
            return True
        except HdfsException as e:
            print(e)
        return False

    def append(self, path, data, **kwargs):
        if not self.exists(path):
            return False
        try:
            self.client.append(path, data, **kwargs)
            return True
        except HdfsException as e:
            print(e)
        return False

    def walk(self, path, topdown=True, onerror=None, **kwargs):
        if not self.exists(path):
            return None
        try:
            ret = self.client.walk(path, topdown, onerror, **kwargs)
            return ret
        except HdfsException as e:
            print(e)
        return None

    def close(self):
        self.client.close()
        print ('close\r\n')

    def rename(self):
        self.client.rename()
        print ('rename\r\n')

    def read(self):
        self.read()
        print ('read\r\n')

def demo():
    GENPicture = 'D:\\ArcClassify\\genPicture\\'
    CMDPath = 'D:\\ArcClassify\\release\\arc.exe'
    hdfsop=hdfs_op(hosts,username)
    print(hdfsop.listdir("/"))
    localsrcmv="C:\\ftpdown\\20170827185234_4_CRH380BL-3737#2_710_0_A.mv"
    localsrcindex="C:\\ftpdown\\20170827185234_4_CRH380BL-3737#2_710_0_A.mv.IDX"
    dest="/20170827185234_4_CRH380BL-3737#2_710_0_A.mv"
    destindex = "/20170827185234_4_CRH380BL-3737#2_710_0_A.mv.IDX"
    src = "/"
    localdest = "C:\\ftpdown\\20170827185234_4_CRH380BL-3737#2_710_0_A1.mv"

    if hdfsop.exists(dest) is True:
        hdfsop.delete(dest)

    print(hdfsop.listdir("/"))
    kwargs={"replication":"1","overwrite":"True"}
    print(hdfsop.upload(localsrcmv,dest,**kwargs))
    print(hdfsop.upload(localsrcindex,destindex,**kwargs))

    walk = hdfsop.walk('/', topdown=False)
#    print (os.walk(walk))
    print (list(walk))
#    with hdfsop.open(dest) as f:
#        cmd = CMDPath+' '+f+' '+GENPicture
#        ret = os.system(cmd)
#        print(ret)

    data ='buffer'
    hdfsop.append(dest, data.encode())
    with hdfsop.open(dest) as f:
        print (f.read())

#    retstatus = hdfsop.file_status("/h2")
#    print (retstatus)
#    print (retstatus.type)


    print(hdfsop.download(dest,localdest))
#    print(hdfsop.file_checksum(dest))
    #print(hdfsop.list_status(dest))
#    ret = hdfsop.file_status(dest)
#    print(ret)

if __name__ == '__main__':
    demo()