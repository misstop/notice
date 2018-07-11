import subprocess
import time
import os
import datetime


# 时间戳转换为时间
def cur_time():
    now = datetime.datetime.now()
    cur_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return cur_time

CYCLE_TIME = 1*60


cmd = 'scrapy crawlall'


i = 0
while True:
    subprocess.Popen(cmd, shell=True if os.name == 'posix' else False)
    i += 1
    time.sleep(CYCLE_TIME)
    print("第{}轮开始执行,{}".format(i, cur_time()))





