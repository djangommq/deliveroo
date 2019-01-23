import os
import csv
from config import DATE
from mongodb_utils import get_db
from utils import VERSION, WEB_NAME,fields

city_list=['hk','au','tw']

filepath=os.path.join(os.path.dirname(__file__),'../crawlerOutput/{}/{}/'.format(VERSION, WEB_NAME))

# 创建链接数据库的对象
client_mongo=get_db()

if __name__ == '__main__':
    for city in city_list:
        info_list=client_mongo.all_items(city)
        if len(info_list)==0:
            continue
        print('导出%s%s数据'%(DATE,city))
        filename=os.path.join(filepath,city+'.csv')
        with open(filename,'a',encoding='utf-8',newline='')as f:
              writer=csv.DictWriter(f,fieldnames=fields)
              if not os.path.getsize(filename):
                    writer.writeheader()
              for info in info_list:
                  writer.writerow(info)