# coding: utf-8
import re
import requests
from pprint import pprint 

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971'
response = requests.get(url, verify=False)
stations = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
f = open("station.py", "w",encoding='utf-8')
pprint(dict(stations), indent=4,stream=f)
print("all done")
f.close()