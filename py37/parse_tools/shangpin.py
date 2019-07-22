# -*- coding: utf-8 -*-
import scrapy
from parse_Tools import get_js_webpage

class ShangpinSpider(scrapy.Spider):
    name = 'shangpin'
    # allowed_domains = ['www.likecha.com']
    start_urls = ['http://www.likecha.com/tools/hscode/loadInstanceList.html?&code=&']

    def parse(self, response):
        res = get_js_webpage(response.url)
        print(res)
