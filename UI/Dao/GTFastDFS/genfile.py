__author__ = 'hejin'

#!/usr/bin/python
from random import randint
import os

data_dir ='E:\\code\\hbase\\fastdfs\\test'
n = 10000
if not os.path.exists(data_dir):
     os.makedirs(data_dir)

for x in range(0, n):
     with open("%s/filetest_%d" % (data_dir, x), 'wb') as fout:
          fout.write(os.urandom(1024 * randint(80, 180)))
