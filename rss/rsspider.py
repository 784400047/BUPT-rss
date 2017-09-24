# -*- coding: utf-8 -*-
#import scrapy
import logging  
import re  
import sys  
import scrapy  
import os
from scrapy.spiders import CrawlSpider, Rule  
from scrapy.linkextractors import LinkExtractor  
from scrapy.http import Request, FormRequest, HtmlResponse  
from scrapy.loader import ItemLoader  
from rss.items import RssItem  
from scrapy import signals
import json
import codecs

class RsspiderSpider(scrapy.Spider):
    name = 'rsspider'
    allowed_domains = ['my.bupt.edu.cn']
    start_urls = ['http://my.bupt.edu.cn/index.portal?.p=Znxjb20ud2lzY29tLnBvcnRhbC5zaXRlLnYyLmltcGwuRnJhZ21lbnRXaW5kb3d8ZjE3MzN8dmlld3xub3JtYWx8Z3JvdXBpZD0xODMyMDIwMDAmZ3JvdXBuYW1lPeaVmeWKoeWkhCZhY3Rpb249YnVsbGV0aW5QYWdlTGlzdA__']

    # 重写了爬虫类的方法, 实现了自定义请求, 运行成功后会调用callback回调函数  
    
      
    # FormRequeset  
    def post_login(self, response):  
        # 先去拿隐藏的表单参数authenticity_token  
        authenticity_token = response.xpath(  
            '//input[@name="lt"]/@value').extract_first()  
        logging.info('lt=' + authenticity_token)  
        pass  

    # 为了模拟浏览器，我们定义httpheader  
    post_headers = {  
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",  
        "Accept-Encoding": "gzip, deflate",  
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",  
        "Cache-Control": "no-cache",  
        "Connection": "keep-alive",  
        "Content-Type": "application/x-www-form-urlencoded",  
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",  
        "Referer": "https://auth.bupt.edu.cn/authserver/login?service=http://my.bupt.edu.cn/index.portal",  
    }  
    # 使用FormRequeset模拟表单提交  
    def post_login(self, response):  
        # 先去拿隐藏的表单参数authenticity_token  
        authenticity_token = response.xpath(  
            '//input[@name="lt"]/@value').extract_first()  
        logging.info('lt=' + authenticity_token)  
        # FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单  
        # 登陆成功后, 会调用after_login回调函数，如果url跟Request页面的一样就省略掉  
        return [FormRequest.from_response(response,  
                                          url='https://auth.bupt.edu.cn/authserver/login?service=http://my.bupt.edu.cn/index.portal',  
                                          meta={'cookiejar': response.meta['cookiejar']},  
                                          headers=self.post_headers,  # 注意此处的headers  
                                          formdata={  
                                              'username': '2017******',#学号  
                                              'password': '*******',  #密码
                                              'lt': authenticity_token,
					      'execution':'e1s1' ,
					      '_eventid':'submit',
					      'rmShown':'1'
                                          },  
                                          callback=self.after_login,  
                                          dont_filter=True  
                                          )]  
      
    def after_login(self, response):  
        # 登录之后，开始进入我要爬取的私信页面  
#        os.system('wget my.bupt.edu.cn/index.portal?.pn=p1778')
        for url in self.start_urls:  
            # 因为我们上面定义了Rule，所以只需要简单的生成初始爬取Request即可  
            yield Request(url, meta={'cookiejar': response.meta['cookiejar']})  
#    def parse(self, response):  
#	l = ItemLoader(item=Product(), response=response)  
#	l.add_xpath('name', '//div[@class="product_name"]')  
#	l.add_xpath('name', '//div[@class="product_title"]')  
#	l.add_xpath('price', '//p[@id="price"]')  
#	l.add_css('stock', 'p#stock]')  
#	l.add_value('last_updated', 'today') # you can also use literal values  
#    return l.load_item()  
    def _requests_to_follow(self, response):  
        """重写加入cookiejar的更新"""  
        if not isinstance(response, HtmlResponse):  
            return  
        seen = set()  
        for n, rule in enumerate(self._rules):  
            links = [l for l in rule.link_extractor.extract_links(response) if l not in seen]  
            if links and rule.process_links:  
                links = rule.process_links(links)  
            for link in links:  
                seen.add(link)  
                r = Request(url=link.url, callback=self._response_downloaded)  
                # 下面这句是我重写的  
                r.meta.update(rule=n, link_text=link.text, cookiejar=response.meta['cookiejar'])  
                yield rule.process_request(r)  
#    def parse_item(self, response):
    def start_requests(self):  
        return [Request("http://my.bupt.edu.cn/",  
                        meta={'cookiejar': 1}, callback=self.post_login)]  
    def parse(self, response):
	self.logger.info('Hi, this is an item page! %s', response.url)
	item = RssItem()
	self.file = codecs.open('rss.xml', 'w', encoding='utf-8')
        item['link']=response.xpath('//a[contains(@href,"pe1144")]/@href').extract()
	item['title']=response.xpath('//a[contains(@href,"pe1144")]/@title').extract()
	line= '<?xml version="1.0" encoding="utf-8"?>'+"\r\n"+'<rss version="2.0">'+"\r\n"+"<channel>"+"\r\n"+"<title>BUPT RSS</title>"+"\r\n"+"<link>my.bupt.edu.cn</link>"+"\r\n"+"<description>BUPT RSS</description>"+"\r\n"
	self.file.write(line) 
#	line = json.dumps(dict(item), ensure_ascii=False) + "\r\n"
        for nn in range(len(item["title"])):
		line = "<item>"+"\r\n"+"<title>"+item['title'][nn]+"</title>"+"\r\n"+"<link>"+"http://my.bupt.edu.cn/"+item['link'][nn]+"</link>"+"\r\n"+"<guid>"+"http://my.bupt.edu.cn/"+item['link'][nn]+"</guid>"+"\r\n"+"</item>"+"\r\n"
		self.file.write(line)       
		self.logger.info(item['link'][nn])
	line ="</channel>"+"\r\n"+"</rss>" 
	self.file.write(line)  
	self.file.close()
        pass
