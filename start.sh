#!/bin/sh
nohup python notice_run.py > /logs/notice/nohup.out 2>&1 &
echo $!>notice.pid
