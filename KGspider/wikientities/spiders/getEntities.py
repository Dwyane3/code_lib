import scrapy
import re
import requests
import time
from requests.adapters import HTTPAdapter
from wikientities.items import WikientitiesItem
import os
'''
class entitiesSpider(scrapy.spiders.Spider):
	name = "entity"
	allowed_domains = ["http://kw.fudan.edu.cn"]
	start_urls = [
		"http://kw.fudan.edu.cn/apis/cndbpedia"
	]

	def containChinese(self,entity):
		zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
		match = zhPattern.search(entity)
		if match:
			return True
		else:
			return False

	def parse(self,response):
		entityList = list()
		#entityCount = 0
		dir_file=os.getcwd()
		dir_file=os.path.join(dir_file,'aaa.txt')
		with open(dir_file,'r',encoding='utf-8') as f:
			for line in f:
				entity = line.split(",")[0]
				entityList.append(entity)
		url_list = list()
		
		count = 0 
		for entity in entityList:
				url = "http://shuyantech.com/api/cndbpedia/avpair?q="+entity
				url_list.append(url)


		headers = {
			"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
			"accept-language" : "zh-CN,zh;q=0.9,en;q=0.8",
			"keep_alive" : "False"
		}
		for url,entity in zip(url_list,entityList):
			
			#print(1.0*count/entityCount)
			#httpRequest = requests.session()
			#httpRequest.keep_alive = False
			httpRequest = requests.session()
			httpRequest.mount('https://', HTTPAdapter(max_retries=30))
			httpRequest.mount('http://', HTTPAdapter(max_retries=30))
			entityjson = httpRequest.get(url,headers=headers).json()
			httpRequest.close()
			if(entityjson['status'] !='fail') and len(entityjson['ret'])!=0:
				tmp = WikientitiesItem()
				tmp['name'] = entity
				tmp['info'] = entityjson['ret']
				yield tmp
			#count += 1
			'''

#############宽度优先爬虫
class entitiesSpider(scrapy.spiders.Spider):
	name = "entity"
	allowed_domains = ["http://kw.fudan.edu.cn"]
	start_urls = [
		"http://kw.fudan.edu.cn/apis/cndbpedia"
	]
	def parse(self,response):
		entityList=[]
		url_list=[]
		##初始化实体列表 
		dir_file=os.getcwd()
		dir_file=os.path.join(dir_file,'aaa.txt')
		with open(dir_file,'r',encoding='utf-8') as f:
			for line in f:
				entity = line.split(",")[0]
				entityList.append(entity)
		for entity in entityList:
			url="http://shuyantech.com/api/cndbpedia/avpair?q="+entity+'&apikey=96d16cb944abac391be5f799e01ef336'
			url_list.append(url)
		###宽度优先
		work=[]
		for url in url_list:
			work.append(url)###初始爬取网页
		###headers
		headers = {
			"accept-language" : "zh-CN,zh;q=0.9,en;q=0.8",
			"keep_alive" : "False"
		}
		while len(work)!=0:
			temp=work.pop(0) ####pop第一个元素，进行爬虫，看是否存在子网页
			httpRequest = requests.session()
			httpRequest.mount('https://', HTTPAdapter(max_retries=30))
			httpRequest.mount('http://', HTTPAdapter(max_retries=30))
			entityjson = httpRequest.get(temp,headers=headers).json()
			httpRequest.close()
			if(entityjson['status'] !='fail') and len(entityjson['ret'])!=0:
				#for a in entityjson['ret']:  ####添加全部子网页
				#	entity2=a[1]
				#	work.append("http://shuyantech.com/api/cndbpedia/avpair?q="+entity2)
				if(len(entityjson['ret'])>=7):
					for i in range(7):          #####添加前7个子网页
						entity2=((entityjson['ret'])[i])[1]
						print(entity2)
						work.append("http://shuyantech.com/api/cndbpedia/avpair?q="+entity2)
				else:
					for a in entityjson['ret']:  ####添加全部子网页
						entity2=a[1]
						work.append("http://shuyantech.com/api/cndbpedia/avpair?q="+entity2+'&apikey=96d16cb944abac391be5f799e01ef336')
				p=re.compile(r'http://shuyantech.com/api/cndbpedia/avpair\?q=(.*)')
				res=p.match(temp)
				tmp = WikientitiesItem()
				tmp['name'] = res.group(1)
				tmp['info'] = entityjson['ret']
				yield tmp