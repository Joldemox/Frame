'''
spider:
1、初始化的url，2、初始请求对象，3、解析数据
'''

from scrapy_plus.http.request import Request
from scrapy_plus.item import Item


class Spider(object):
    name = ''

    # 标示增量式爬虫,存在延时阻塞的即为增量式爬虫，默认为False
    time_task = False

    # 1、初始化的url
    start_urls = []

    # 2、初始请求对象
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    # 3、解析数据
    def parse(self, response):
        yield Item(response.url)
