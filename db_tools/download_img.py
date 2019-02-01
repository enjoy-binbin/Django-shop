import pymongo
import requests
import sys
import os

client = pymongo.MongoClient('localhost')
db = client['suning']
goods = db['goods']

for good in goods.find():
    print(good['good_img'])
    html = requests.get('http:'+good['good_img'])
    name = good['good_name'].replace('/', ' ').replace('苏宁超市自营', '').replace('（', '').replace('）', '').replace(':', '比').replace('*','X').replace('|', ' ').strip()
    with open(os.path.join(name + '.jpg'), 'wb') as ff:
        ff.write(html.content)