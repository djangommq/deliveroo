# encoding=utf8
import logging
import requests
import time
import csv
import os
import sys

from numpy import arange
import json
from math import radians, cos, sin, asin, sqrt
import numpy as np
from utils import VERSION, WEB_NAME
from mongodb_utils import get_db

# 创建连接数据库的链接对象
client_mongo=get_db()

# Define a basic Haversine distance formula半正矢计算坐标距离
def haversine(lat1, lon1, lat2, lon2):
    MILES = 3959
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    total_miles = MILES * c
    return total_miles


# 计算两点间距离-m
def geodistance(lng1, lat1, lng2, lat2):
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])
    dlon = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    dis = 2 * asin(sqrt(a)) * 6371 * 1000
    return dis


date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
print(date)


def get_city_info(id):
    input_path = './input_data/locations.csv'
    with open(input_path, 'r') as fr:
        csv_f = csv.DictReader(fr)
        for row in csv_f:
            if csv_f.line_num == 1:
                continue
            if int(row.get('id')) == id:
                return dict(row)
        return None


def save_success_city(city):
    file_path = '../crawlerOutput/{}/{}/has_get_city.txt'.format(VERSION, WEB_NAME)
    with open(file_path, 'a') as f:
        f.writelines(city + '\n')


def load_success_cities():
    file_path = '../crawlerOutput/{}/{}/has_get_city.txt'.format(VERSION, WEB_NAME)
    try:
        with open(file_path, 'r') as f:
            s = f.readlines()
            return s
    except:
        return []


def get_city_detail(city):
    city_name = city.get('city_name')
    lat_top_left = city.get('lat_top_left')
    lng_top_left = city.get('lng_top_left')
    lat_bottom_right = city.get('lat_bottom_right')
    lng_bottom_right = city.get('lng_bottom_right')

    for lat in arange(float(lat_top_left), float(lat_bottom_right), -0.01):
        for lng in arange(float(lng_top_left), float(lng_bottom_right), 0.01):
            try:
                lat = round(lat, 6)
                lng = round(lng, 6)
                print("checking restaurants around " + str(lat) + "/" + str(lng), "........")

                data = {'lat': lat, 'lng': lng}
                header = {
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    # 'Cookie' : 'roo_guid=ED532102-03E2-4EC2-899C-6A190F91A35B; roo_session_guid=eaa2da63-4d4c-420f-b529-9db8c605fc4a; roo_super_properties=eyJBcHBsZSBQYXkgU3RhdHVzIjoiYXZhaWxhYmxlIiwiQ2FtcGFpZ24gTWVkaXVtIjoibm9uZSIsIm12dF8zNF9pb3NfbGl2ZV9jaGF0X2VuYWJsZWRfc2ciOiJ0cnVlIiwibXZ0XzM5X2lvc19hcHBsZV9wYXlfYWNjb3VudF9jcmVhdGlvbl9oayI6ImRpc2FibGVkIiwiTG9jYWxlIjoiemgiLCJMb2NhdGlvbiBQZXJtaXNzaW9ucyI6ImF1dGhvcml6ZWQiLCJEZXZpY2UgVHlwZSI6InBob25lIiwiSVAgRGV0ZWN0ZWQgQ291bnRyeSAoSW5hY2N1cmF0ZSkiOiJTRyIsImNvbnRleHQiOnsidXNlckFnZW50IjoiRGVsaXZlcm9vLU9yZGVyQXBwXC8yLjcuMCAoaVBob25lNywxOyBpT1MxMC4xLjE7IFJlbGVhc2U7IHpoX0NOOyA2MDg4KSIsImlwIjoiMTExLjY1LjM2LjQ3IiwiY2FtcGFpZ24iOnsibmFtZSI6ImRpcmVjdCIsInNvdXJjZSI6ImRpcmVjdCIsIm1lZGl1bSI6Im5vbmUifX0sIm12dF8zNF9pb3NfbGl2ZV9jaGF0X2VuYWJsZWRfZnIiOiJ0cnVlIiwibXZ0XzM0X2lvc19saXZlX2NoYXRfZW5hYmxlZF91ayI6InRydWUiLCJtdnRfMzlfaW9zX2FwcGxlX3BheV9hY2NvdW50X2NyZWF0aW9uX2VzIjoiZGlzYWJsZWQiLCJtdnRfMTc5X2lvc19sb2FkaW5nX3NwaW5uZXJfd2hlbl9sb2NhdGlvbl9jaGFuZ2VzIjoib3JpZ2luYWwiLCJDYW1wYWlnbiBOYW1lIjoiZGlyZWN0IiwiQXBwIFZlcnNpb24iOiIyLjcuMCIsIm12dF8zNF9pb3NfbGl2ZV9jaGF0X2VuYWJsZWRfZXMiOiJ0cnVlIiwiUGxhdGZvcm0iOiJpT1MiLCJtdnRfMzlfaW9zX2FwcGxlX3BheV9hY2NvdW50X2NyZWF0aW9uX2F1IjoiZGlzYWJsZWQiLCJtdnRfMTkxX2lvc19yZXN0YXVyYW50X2Rlc2NyaXB0aW9uIjoiY29sbGFwc2VkIiwibXZ0XzM0X2lvc19saXZlX2NoYXRfZW5hYmxlZF9pdCI6InRydWUiLCJtdnRfMzlfaW9zX2FwcGxlX3BheV9hY2NvdW50X2NyZWF0aW9uX3NnIjoiZW5hYmxlZCIsIm12dF8zOV9pb3NfYXBwbGVfcGF5X2FjY291bnRfY3JlYXRpb25fdWsiOiJlbmFibGVkIiwibXZ0XzM3X25ld19hZGRyZXNzX2Zsb3ciOiJ0cnVlIiwiUm9vQnJvd3NlclZlcnNpb24iOiIwIiwibXZ0XzE5Ml9pb3NfZGlzaF9zZWFyY2hfb25fbWVudSI6ImNvbnRyb2wiLCJBcHAgTmFtZXNwYWNlIjoiY29tLmRlbGl2ZXJvby5vcmRlcmFwcCIsIkNhbXBhaWduIFNvdXJjZSI6ImRpcmVjdCIsIlRMRCI6ImhrIiwiUmVxdWVzdGVkIExvY2FsZSI6InpoIiwibXZ0XzM0X2lvc19saXZlX2NoYXRfZW5hYmxlZF9kZSI6InRydWUiLCJtdnRfMTk4X2lvc19yZW9yZGVyX3ZpZXciOiJjb250cm9sIiwibXZ0XzM0X2lvc19saXZlX2NoYXRfZW5hYmxlZF9hdSI6InRydWUiLCJEZXZpY2UgTW9kZWwiOiJpUGhvbmU3LDEiLCJtdnRfMTM1X2lvc19yZXN0YXVyYW50X2ltYWdlX2hlaWdodCI6Im9yaWdpbmFsIiwibXZ0XzM0X2lvc19saXZlX2NoYXRfZW5hYmxlZF9pZSI6InRydWUiLCJtdnRfMzlfaW9zX2FwcGxlX3BheV9hY2NvdW50X2NyZWF0aW9uX2ZyIjoiZGlzYWJsZWQiLCJPUyBWZXJzaW9uIjoiMTAuMS4xIiwibXZ0XzE0MF9pb3Nfc3dhcF9vcmRlcl9vZl9zaWduX3VwX2FuZF9zaWduX2luX2Zvcl9ob21lc2NyZWVuIjoib3JpZ2luYWwiLCJJREZBIjoiMDM5MDEwMzgtMEU0MS00NTdDLTkzMzgtQzAyODg3MjcxQ0NCIiwibXZ0XzkzX2lvc19kZWxpdmVyeV9zZWxlY3Rvcl9wb3NpdGlvbiI6Im9uX3RvcCIsIm12dF8zNF9pb3NfbGl2ZV9jaGF0X2VuYWJsZWRfbmwiOiJ0cnVlIiwibXZ0XzM0X2lvc19saXZlX2NoYXRfZW5hYmxlZF9oayI6InRydWUiLCJJREZWIjoiOTFBRjUzRkItRTRDRC00NzA4LUFGQjUtOThCRjA3MjJGODFBIiwiUm9vQnJvd3NlciI6IkdlbmVyaWMgQnJvd3NlciIsIm12dF8xMjFfaW9zX3N3YXBfb3JkZXJfb2Zfc2lnbl91cF9hbmRfc2lnbl9pbiI6InNpZ251cF9iZWZvcmVfc2lnbl9pbiIsIm12dF8xODJfaW9zX2NvbGxlY3Rpb25fdGFnc192aXNpYmlsaXR5IjoiaGlkZV9jb2xsZWN0aW9uc190YWdzIn0.',
                    # 'Authorization' : 'Basic NDI3OTk4NDpvcmRlcmFwcF9pb3MsZDk5NWUzNWYyMTkwNDFkZTk3NzU5MDdmNTMwNTZiNDM=',
                    'Accept': '*/*',
                    'X-Roo-Country': 'hk',
                    'User-Agent': 'Deliveroo-OrderApp/2.7.0 (iPhone7,1; iOS10.1.1; Release; 6088)',
                    'App-version': 'gzip, deflate'
                }
                response = requests.get('http://deliveroo.co.uk/orderapp/v1/restaurants', headers=header, params=data)
                content = response.text
                # 日志写入
                if content=='{"banners":[],"featured":[],"restaurants":[],"user":{}}':
                    logging.error(str(response.status_code)+'\t\t'+'lat:'+str(lat)+'\tlng:'+str(lng)+'\t\t无数据')
                else:
                    logging.error(str(response.status_code)+'\t\t'+'lat:'+str(lat)+'\tlng:'+str(lng)+'\t\t有数据')

                if response.status_code != 200:
                    continue
                json_dict = json.loads(content, encoding='utf-8')
                # process the content
                country = json_dict.get('zone').get('country')
                if country is None:
                    continue
                else:
                    now_city = country.get('tld')
                if len(json_dict['restaurants']) > 0:
                    for i in range(0, len(json_dict['restaurants'])):
                        print(len(json_dict['restaurants']))
                        only_on_deliveroo = False
                        free_delivery = False
                        if len(json_dict['restaurants'][i]['menu']['menu_tags']) > 0:
                            for tag_num in range(0, len(json_dict['restaurants'][i]['menu']['menu_tags'])):
                                if json_dict['restaurants'][i]['menu']['menu_tags'][tag_num][
                                    'name'] == 'Only On Deliveroo':
                                    only_on_deliveroo = True
                                if json_dict['restaurants'][i]['menu']['menu_tags'][tag_num][
                                    'name'] == 'Free Deliveroo':
                                    free_delivery = True
                            print('ok')

                        data_frame = {
                            # date of the week when we run the tool
                            'running_date': '2019-01-01 00:05:10',
                            # the lat/lng when we 'open' the app and the restaurants shown in app are around this lat/lng point
                            'request_lat': lat,
                            'request_lng': lng,

                            # response data
                            # restaurant info
                            'city_name': now_city,
                            'resto_id': json_dict['restaurants'][i]['id'],
                            'resto_name': json_dict['restaurants'][i]['name'],
                            'resto_name_with_branch': json_dict['restaurants'][i]['name_with_branch'] if (
                                    type(json_dict['restaurants'][i]['name_with_branch']) == str) else '',
                            'rank_in_app': i,
                            'resto_uname': json_dict['restaurants'][i]['uname'],

                            'price_category': json_dict['restaurants'][i]['price_category'],
                            'currency_symbol': json_dict['restaurants'][i]['currency_symbol'],
                            'only_on_deliveroo': only_on_deliveroo,
                            'free_delivery': free_delivery,
                            'neighborhood_id': json_dict['restaurants'][i]['neighborhood']['id'],
                            'neighborhood_name': json_dict['restaurants'][i]['neighborhood']['name'],
                            'neighborhood_uname': json_dict['restaurants'][i]['neighborhood']['uname'],

                            'resto_lat': json_dict['restaurants'][i]['coordinates'][1],
                            'resto_lng': json_dict['restaurants'][i]['coordinates'][0],
                            'newly_added': json_dict['restaurants'][i]['newly_added'],
                            'category': json_dict['restaurants'][i]['category'] if (
                                    type(json_dict['restaurants'][i]['category']) == str) else '',
                            'curr_prep_time': json_dict['restaurants'][i]['curr_prep_time'],
                            'delay_time': json_dict['restaurants'][i]['delay_time'],
                            'baseline_deliver_time': json_dict['restaurants'][i]['baseline_deliver_time'],
                            'total_time': json_dict['restaurants'][i]['total_time'],
                            'distance_m': json_dict['restaurants'][i]['distance_m'],
                            'travel_time': json_dict['restaurants'][i]['travel_time'],
                            'target_delivery_time': json_dict['restaurants'][i]['target_delivery_time']['minutes'],

                            # eater to resto dispatch distance, calculated based on request lng/lat and resto lat/lng
                            # unit: km
                            'eater_resto_dispatch_distance_km': haversine(lat, lng, json_dict['restaurants'][i][
                                'coordinates'][1], json_dict['restaurants'][i]['coordinates'][0])
                            # R语言半正矢计算经纬度距离   distm (c(lng, lat), c(json_dict['restaurants'][i]['coordinates'][1], json_dict['restaurants'][i]['coordinates'][2]), fun = distHaversine)/1000
                        }
                        save_to_csv(data_frame)

            except Exception as e:
                pass
    save_success_city(city_name)


def save_to_csv(data):
    # 路径: ../crawlerOutput/deliveroo/20180801/singapore.csv
    city_name = data.get('city_name')
    output_path = '../crawlerOutput/{}/{}/{}.csv'.format(VERSION, WEB_NAME, city_name)
    output_dir = os.path.split(output_path)[0]
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # 先创建目录, 再写入表头
    # if not os.path.exists(output_path):
    #     with open(output_path, 'a', encoding='utf-8', newline='') as f:
    #         csv_f = csv.DictWriter(f, fieldnames=fields)
    #         csv_f.writeheader()
    # with open(output_path, 'a', encoding='utf-8', newline='') as f:
    #     csv_f = csv.DictWriter(f, fieldnames=fields)
    #     csv_f.writerow(data)
    # 将数据保存到mongo数据库
    client_mongo.insert_one(city_name,data,condition=['resto_id'])

if __name__ == '__main__':
    if len(sys.argv) <2:
        id = 6
    else:
        id = int(sys.argv[1])
    city = get_city_info(id)
    if city is None:
        print('参数输入错误, 范围: 1-18, 详见input/location.csv')
    print(city)
    get_city_detail(city)