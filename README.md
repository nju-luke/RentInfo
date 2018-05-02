# RentInfo

按照指定条件，爬取58同城的租房信息，并将结果保存到mangodb中。

满足条件的状态为0，不满足条件的状态为4。

mango以目标网址保存，爬取过后下次自动跳过。

***使用前请指定百度lbs账户ak，设置城市及对应区域。***

### 启动方式：

```shell
cd RentInfo/spider/tc58
scrapy crawl tc58
```

### 城市区域设置方式：

路径： RentInfo/spider/tc58/tc58/data/regions

### 指定条件及路径：

路径: RentInfo/spider/tc58/tc58/utils

```python

MINPRICE = 2000     # 最低价格
MAXPRICE = 3500     # 最高价格
MAXDISTANCE = 7     # 距离目标地点与可选地点之间的距离之和
CITY = "上海"         # 城市
NB_ROOM = {'1室', '2室', }    # 房间数

COOKIE = None
proxies = [
    "http://localhost:1087",
    ''
]                       # 代理地址

ak = "" #百度lbs服务key，请自行申请（http://lbsyun.baidu.com/apiconsole/key）
# 若使用其他lbs服务，请同时修改pipelines中的 get_lbs 函数

# GPS， (longitude，latitude）
# primary
GPS1 = {"lat": 31.239777,
        "lng": 121.669717}  # 目标地点的gps信息
# Secondary                 # 可选地点gps信息
GPS2 = [
    # {"lat": 31.219828,
    #  "lng": 121.662625},  # 唐镇地铁站
    # {"lat": 31.216703,
    #  "lng": 121.627179},  # 广兰路地铁站
    {"lat": 31.269485,
     "lng": 121.64549},  # 金海路地铁站
    {"lat": 31.272188,
     "lng": 121.663},  # 顾唐路地铁站
    {"lat": 31.274649,
     "lng": 121.674609},  # 明雷路地铁站
    {"lat": 31.26994,
     "lng": 121.634401}  # 金吉路地铁站
]
locations = [              # 与GPS2对应的地点名
    # "唐镇地铁站",
    # "广兰路地铁站",
    "金海路地铁站",
    "顾唐路地铁站",
    "明雷路地铁站",
    "金吉路地铁站",
]


def get_collection(host, db, collection):
    client = pymongo.MongoClient(host)
    db = client[db]
    collection = db[collection]
    return collection

collection = get_collection('localhost', 'mydb', 'rent_info')       # 保存mango表信息

```

