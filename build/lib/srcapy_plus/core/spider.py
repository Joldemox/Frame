'''
spider:
1、初始化的url，2、初始请求对象，3、解析数据
'''

from scrapy_plus.http.request import Request
from scrapy_plus.item import Item


class Spider(object):
    # 1、初始化的url
    start_url = 'http://www.baidu.com'

    # 2、初始请求对象
    def start_request(self):
        return Request(self.start_url)

    # 3、解析数据
    def parse(self, response):
        return Item(response.url)
