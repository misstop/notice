import subprocess
import time
import os
import datetime
import logging


# 时间戳转换为时间
def cur_time():
    now = datetime.datetime.now()
    cur_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return cur_time

# 3分钟拉一次
CYCLE_TIME = 3 * 60


cmd = 'scrapy crawlall'


i = 1
while True:
    logging.info("第{}轮开始执行,{}".format(i, cur_time()))
    print("第{}轮开始执行,{}".format(i, cur_time()))
    subprocess.Popen(cmd, shell=True if os.name == 'posix' else False)
    i += 1
    time.sleep(CYCLE_TIME)





