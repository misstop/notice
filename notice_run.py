import subprocess
import time
import os
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# 时间戳转换为时间
def cur_time():
    now = datetime.datetime.now()
    cur_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return cur_time


cmd = 'scrapy crawlall'
i = 0


def run():
    global i
    subprocess.Popen(cmd, shell=True if os.name == 'posix' else False)
    i += 1
    print("第{}轮开始执行,{}".format(i, cur_time()))


SCHEDULER = BlockingScheduler()
if __name__ == '__main__':
    SCHEDULER.add_job(func=run, trigger='interval', minutes=2)
    SCHEDULER.start()


