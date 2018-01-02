#!/bin/bash
pid=`ps -ef | grep error_monitor.py | grep -v grep | awk '{print $2}'`
count=`ps -ef | grep error_monitor.py | grep -v grep | wc -l`
if [ ${count} -lt 1 ]
then
    python error_monitor.py $1 $2 &
else
    echo "has error_monitor.py, pid=${pid}"
fi
