# deliveroo

## 基本情况
1. 起始于： 2018年7月   
2. 相关国家和地区： 南非


## API的获取


## 代码地址
[gitlab](https://gitlab.yunfutech.com/uber_crawler/Deliveroo.git)  
脚本操作见 readme.md


## 进展
2018-07-30： 欧非要求的国家和地区:  
- Australia  
- Belgium  
- France  
- Germany  
- Hong Kong  
- Ireland  
- Italy  
- Netherlands  
- Singapore  
- Spain  
- UK  
- United Arab Emirates  

2018-10-30: 亚太区要求的
- Australia  
- Hong Kong  
- Taiwan
澳大利亚和香港, 欧非区和亚太区共享

## 追加要求
12/12 Chase邮件通知, 欧非区不再要求提交数据
2018-12月份 Ken邮件通知 , deliveroo数据整体偏少
        0.02 * 0.02
        au: 8456
        hk: 1652
        tw: 447

2019-1月份 将经纬度跨度改为0.01*0.01
2019-1月份 数据保存至数据库,添加测试脚本(测试地区为香港的部分区域)
...

## 爬虫运行服务器安排
```
服务器                 id

法兰克福1              6,20
法兰克福2               21
法兰克福3               22
法兰克福4               23
法兰克福5               24
法兰克福6               25
法兰克福7               26
法兰克福8               27
法兰克福9               28
法兰克福10             29,30

爬虫运行时间为4天左右
```



## 使用说明(每次启动修改config.py中的日期)
1. 每次启动deliveroo_start.py 即可, 数据输出到: ../../crawlerOutput/latest/deliveroo/

2. 获取数据时, 将latest修改为当前日期, 以便下次运行时, 数据输出到全新的latest文件夹

## 数据有效性验证

8月份去重后结果: 39622


## 脚本说明
之前脚本来自亚太区, 8月份欧菲要求, 进行了重构
1. 添加log日志, 位于
```
'../../crawlerOutput/latest/log/deliveroo.log'
```
2. 重构代码结构, 分块, 并添加了停止继续功能.
3. input说明
对每个地区进行了编号, 每次启动后缀带id即可
这样可以单独运行, 编写一个shell脚本可一键前部启动


### 数据保存
```
数据保存在东京0上的mongo数据库中

```