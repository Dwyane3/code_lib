import scrapy
import re
import requests
import time
from requests.adapters import HTTPAdapter
from wikientities.items import WikientitiesItem
import os
from scrapy.exceptions import CloseSpider
'''
class entitiesSpider(scrapy.spiders.Spider):
	name = "entity"
	allowed_domains = ["http://kw.fudan.edu.cn"]
	start_urls = [
		"http://shuyantech.com/api/cndbpedia"
	]
	handle_httpstatus_list = [404]

	#def containChinese(self,entity):
	#	zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
	#	match = zhPattern.search(entity)
	#	if match:
	#		return True
	#	else:
	#		return False
#
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
		
		#count = 0 
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
	allowed_domains = ["shuyantech.com"]
	start_urls = [
		"http://shuyantech.com/api/cndbpedia/avpair?q="
	]
	def parse(self,response):
		count=0	##记录爬取次数 
		entityList=[]
		url_list=[]
		##初始化实体列表 
		dir_file=os.getcwd()
		dir_file=os.path.join(dir_file,'bbb.txt')
		with open(dir_file,'r',encoding='utf-8') as f:
			for line in f:
				entity = line.split(",")[0]
				entityList.append(entity)
		for entity in entityList:
			url="http://shuyantech.com/api/cndbpedia/avpair?q="+entity+'&apikey=96d16cb944abac391be5f799e01ef336'
			url_list.append(url)
		###宽度优先
		#print(url_list,'***url*****')
		work=[]
		existed=[]
		for url in url_list:
			work.append(url)###初始爬取网页
		###headers
		headers = {
			"user-agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
			"accept-language" : "zh-CN,zh;q=0.9,en;q=0.8",
			"keep_alive" : "False"
		}
		while len(work)!=0:
			flag=1 ####代表写入该实体所有相关实体
			#print(work,'*********work**************')
			temp=work.pop(0) ####pop第一个元素，进行爬虫，看是否存在子网页
			#print(existed,'******existed*')
			#print(temp,'******temp********')
			count+=1
			httpRequest = requests.session()
			httpRequest.mount('https://', HTTPAdapter(max_retries=30))
			httpRequest.mount('http://', HTTPAdapter(max_retries=30))
			entityjson = httpRequest.get(temp,headers=headers).json()
			httpRequest.close()
			print(entityjson)
			existed.append(temp)
			if(entityjson['status'] !='fail') and len(entityjson['ret'])!=0:
				if(len(entityjson['ret'])>=7):
					sum=0
					flag=0 ###代表只写入该实体前7个不重复的相关实体
					for i in range(7):          #####添加前5个子网页
						entity1=((entityjson['ret'])[i])[0]
						entity2=((entityjson['ret'])[i])[1]
						print(entity1)
						if "http://shuyantech.com/api/cndbpedia/avpair?q="+entity2+'&apikey=96d16cb944abac391be5f799e01ef336' not in work and "http://shuyantech.com/api/cndbpedia/avpair?q="+entity2+'&apikey=96d16cb944abac391be5f799e01ef336'not in existed:
							#print('实体：'+entity2+'已添加到工作队列...')
							sum+=1
							work.append("http://shuyantech.com/api/cndbpedia/avpair?q="+entity2+'&apikey=96d16cb944abac391be5f799e01ef336')
				else:
					flag=1 ####
					for a in entityjson['ret']:  ####添加全部子网页
						entity2=a[1]
						if "http://shuyantech.com/api/cndbpedia/avpair?q="+entity2+'&apikey=96d16cb944abac391be5f799e01ef336' not in work and "http://shuyantech.com/api/cndbpedia/avpair?q="+entity2+'&apikey=96d16cb944abac391be5f799e01ef336'not in existed:
							work.append("http://shuyantech.com/api/cndbpedia/avpair?q="+entity2+'&apikey=96d16cb944abac391be5f799e01ef336')
			else :
				raise CloseSpider('api调用异常...')
			p=re.compile(r'http://shuyantech.com/api/cndbpedia/avpair\?q=(.*)&apikey=96d16cb944abac391be5f799e01ef336')
			res=p.match(temp)
			if res==None:#####实体中有转义字符，跳过#####
				tmp = WikientitiesItem()
				tmp['name'] = 'NA'
				tmp['info'] = 'NA'
				yield tmp
			elif flag==1:
				tmp = WikientitiesItem()
				tmp['name'] = res.group(1)
				tmp['info'] = entityjson['ret']
				yield tmp
			else:
				tmp = WikientitiesItem()
				tmp['name'] = res.group(1)
				tmp['info'] = (entityjson['ret'])[7-sum:7]####从sum到第7个
				yield tmp
			#print(count)
			if count==5000:
				raise CloseSpider('已调用api 5000次...限制为5000次/h')
		if len(work)==0:
			raise CloseSpider('队列为空...')