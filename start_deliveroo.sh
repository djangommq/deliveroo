#!/bin/sh
# 启动爬虫
/usr/bin/python3 /home/ec2-user/crawler/Deliveroo/deliveroo.py 1 >/dev/null 2>&1 &
/usr/bin/python3 /home/ec2-user/crawler/Deliveroo/deliveroo.py 2 >/dev/null 2>&1 &
/usr/bin/python3 /home/ec2-user/crawler/Deliveroo/deliveroo.py 3 >/dev/null 2>&1 &
/usr/bin/python3 /home/ec2-user/crawler/Deliveroo/deliveroo.py 4 >/dev/null 2>&1 &
/usr/bin/python3 /home/ec2-user/crawler/Deliveroo/deliveroo.py 5 >/dev/null 2>&1 &
/usr/bin/python3 /home/ec2-user/crawler/Deliveroo/deliveroo.py 6 >/dev/null 2>&1 &
/usr/bin/python3 /home/ec2-user/crawler/Deliveroo/deliveroo.py 7 >/dev/null 2>&1 &

# 去重
/usr/bin/python3 /home/ec2-user/crawler/Deliveroo/deduplicate.py >/dev/null 2>&1