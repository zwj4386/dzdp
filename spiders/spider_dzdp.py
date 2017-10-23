# coding=utf-8
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import sys
import os
from dzdp.items import DzdpItem
import pymysql
import time
from fake_useragent import UserAgent
reload(sys)
sys.setdefaultencoding('utf-8')

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class spider_dzdp(scrapy.Spider):
    name = 'dzdp'
    start_urls = ['http://www.dianping.com']
    allowed_domain = 'www.dianping.com'

    conn = pymysql.connect(host='192.168.3.232', port=3306, user='zwj', passwd='123456', db='caiji',
                           charset='utf8')
    cursor = conn.cursor()

    def parse(self, response):
        #从选项栏获取单个种类的src yield Request一个50页的列表 再请求进一个子网页拿数据
        #到韩国料理 。。。
        sql = 'select href,fenlei from DZDP_URLLIST'
        self.cursor.execute(sql)
        rs = self.cursor.fetchall()

        for i in range(0,len(rs)):
            u = rs[i][0]
            fenlei = rs[i][1]
            yield Request(u,meta={'fenlei':fenlei},callback=self.getDetailUrl)


    def getDetailUrl(self,response):
        xp = Selector(response)
        div = xp.xpath("//div[@class='shop-list J_shop-list shop-all-list']/ul/li")
        fenlei = response.meta['fenlei']
        ua = UserAgent()
        for i in div:
            href = i.xpath('./div[@class="txt"]/div[@class="tit"]/a/@href')[0].extract()
            sql = 'select 1 from DZDP where HREF="%s"'%href
            self.cursor.execute(sql)
            rs = self.cursor.fetchall()
            if len(rs)==0:
                useragent = ua.random
                headers = { 'User-Agent':useragent}
                yield Request(href,headers=headers, meta={'href':href,'fenlei':fenlei},callback=self.getItem)
            else:
                continue

        next = xp.xpath('//a[@class="next"]/@href').extract()
        if len(next)!=0:
            next_url=''.join(next)
            yield Request(next_url, meta={'href':href,'fenlei':fenlei},callback=self.getDetailUrl)

    def getItem(self,response):
        item = DzdpItem()
        hx = Selector(response)
        href = response.meta['href']

        name = ''.join(hx.xpath("//h1[@class='shop-name']/text()").extract()).encode('utf-8').replace('\n','').strip()
        comment = ''.join(hx.xpath('//div[@class="brief-info"]/span[@id="reviewCount"]/text()').extract()).encode('utf-8').replace('\n','').strip()
        cpp = ''.join(hx.xpath('//div[@class="brief-info"]/span[@id="avgPriceTitle"]/text()').extract()).encode('utf-8').replace('\n','').strip()
        flag = hx.xpath('//span[@id="comment_score"]/span[@class="item"]/text()')
        if len(flag)<>0:
            score = ''.join(hx.xpath('//span[@id="comment_score"]/span[@class="item"]/text()')[0].extract()).encode(
                'utf-8').replace('\n', '').strip()
            envir = ''.join(hx.xpath('//span[@id="comment_score"]/span[@class="item"]/text()')[1].extract()).encode(
                'utf-8').replace('\n', '').strip()
        else:
            score = ''
            envir = ''
        addr = ''.join(hx.xpath('//div[@class="expand-info address"]/span[@class="item"]/text()').extract()).encode('utf-8').replace('\n','').strip()
        pcount = hx.xpath('//p[@class="expand-info tel"]/span[@class="item"]')
        if len(pcount)==2:
            phone = ''.join(hx.xpath('//p[@class="expand-info tel"]/span[@class="item"]/text()')[0].extract()).encode('utf-8').replace('\n','').strip()+' '+\
                    ''.join(hx.xpath('//p[@class="expand-info tel"]/span[@class="item"]/text()')[1].extract()).encode('utf-8').replace('\n', '').strip()
        else:
            phone = ''.join(hx.xpath('//p[@class="expand-info tel"]/span[@class="item"]/text()').extract()).encode('utf-8').replace('\n','').strip()
        cjmc = response.meta['fenlei']
        city = r'合肥'
        item['name'] = name
        item['comment'] = comment
        item['cpp'] = cpp
        item['score'] = score
        item['envir'] = envir
        item['addr'] = addr
        item['phone'] = phone
        item['cjmc'] = cjmc
        item['city'] = city
        item['href'] = href

        if item['name']<>'' and item['name']<>None:
            yield item
        else:
            pass



