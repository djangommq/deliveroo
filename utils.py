import os
import logging

WEB_NAME = 'deliveroo'
VERSION = 'latest'

fields = [
    'running_date',
    'request_lat',
    'request_lng',
    'city_name',
    'resto_id',
    'resto_name',
    'resto_name_with_branch',
    'rank_in_app',
    'resto_uname',
    'price_category',
    'currency_symbol',
    'only_on_deliveroo',
    'free_delivery',
    'neighborhood_id',
    'neighborhood_name',
    'neighborhood_uname',
    'resto_lat',
    'resto_lng',
    'newly_added',
    'category',
    'curr_prep_time',
    'delay_time',
    'baseline_deliver_time',
    'total_time',
    'distance_m',
    'travel_time',
    'target_delivery_time',
    'eater_resto_dispatch_distance_km'
]


log_path = '../crawlerOutput/{}/log/{}.log'.format(VERSION, WEB_NAME)
log_dir = os.path.split(log_path)[0]
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(filename=log_path,
                    level=logging.ERROR,
                    filemode='a',
                    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',    # 定义输出log的格式
                    datefmt='%Y-%m-%d %A %H:%M:%S'
                    )
logger_name = '{}_log'.format(WEB_NAME)
logger = logging.getLogger(logger_name)