# -*- coding: utf-8 -*-
import scrapy
from example.parse_Tools import get_js_webpage

class ShangpinSpider(scrapy.Spider):
    name = 'shangpin'
    allowed_domains = ['www.likecha.com']
    start_urls = ['http://www.likecha.com/tools/hscode/loadInstanceList.html?&code=&pageIndex=1']

    def parse(self, response):
        # res = get_js_webpage(response.url)
        page_count = response.xpath('//div[@class="casepage"]').xpath('string(.)').extract_first().split('共')[1].split('页')[0]
        for i in range(int(page_count)):

            page = response.xpath('//div[@class="casewrap"]').xpath('string(.)').extract_first()
        print(page)
