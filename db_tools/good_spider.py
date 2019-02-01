from bs4 import BeautifulSoup 
from selenium import webdriver
import pymongo, time

client = pymongo.MongoClient('localhost')
db = client['suning']
table = db['goods'].drop()

url = ('https://search.suning.com/奶粉/')
driver=webdriver.Firefox()
driver.maximize_window()
# WebDriverWait(driver, 100).until(lambda x: x.find_element_by_xpath('.WB_FEED'))
# driver.implicitly_wait(20)  # 隐性等待时间，等待price加载
driver.get(url)
js="var q=document.documentElement.scrollTop=2000;"  
driver.execute_script(js)  # 拉动滚动条，加载price
time.sleep(7)  # 强制睡一会等待price加载
soup = BeautifulSoup(driver.page_source, 'lxml')
lis = soup.select('li.item-wrap')
i = 1  # 只抓25条
for li in lis:
	if i == 26:
		break
	i+=1
	good_name = li.select('img')[0]['alt']
	good_img = li.select('img')[0]['src']
	good_price = li.select('.def-price')[0].get_text()
	good = {'good_name': good_name, 'good_price': good_price, 'good_img': good_img}
	db['goods'].insert(good)
	print(good_name + '插入mongo成功')

driver.close()