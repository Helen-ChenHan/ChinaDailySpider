from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from craigslist_sample.items import CNDItem
import scrapy
import re
import os.path
from scrapy.utils.response import body_or_str

class MySpider(CrawlSpider):
    name = "cnd"
    allowed_domains = ["usa.chinadaily.com.cn"]
    start_urls = ["http://usa.chinadaily.com.cn/"]

    rules = (
        Rule(LinkExtractor(allow=('')), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = Selector(response)
        items = []
        item = CNDItem()
        item["title"] = hxs.xpath('//h2/text()').extract()[0]
        article = hxs.xpath('string(//div[contains(@class, "articl-sub") or contains(@id, "Content")])').extract()
        item["article"] = "\n".join(article).encode('utf8')
        item["link"] = response.url
        item["date"] = hxs.xpath('//h5/text()').extract()[0]
        items.append(item)
        return(items)