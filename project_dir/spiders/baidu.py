from scrapy_plus.core.spider import Spider
from scrapy_plus.http.request import Request
from scrapy_plus.item import Item


class BaiduSpider(Spider):
    name = 'baidu'
    # start_url = 'https://www.baidu.com/'
    start_urls = [
        'http://www.itcast.cn/',
        'http://www.so.com/',
        'http://www.baidu.com/',
        'http://v.baidu.com/',
        'http://www.so.com/',
        'http://www.so.com/',
    ]

# class BaiduSpider(Spider):
#     name = 'baidu'
#     start_urls = ['http://www.baidu.com']
#     total = 0
#
#     def parse(self, response):
#         self.total += 1
#         if self.total > 10:
#             return
#         yield Request(self.start_urls[0], filter=False, parse='parse')


# baidu2
# 增量式爬虫的示例
# import time
#
#
# class BaiduSpider(Spider):
#     name = 'baidu'
#     start_urls = ['https://www.baidu.com']
#     timed_task = True  # 表示 这是一个定时爬虫
#
#     def start_requests(self):
#         while True:
#             for url in self.start_urls:
#                 yield Request(url, parse='parse', filter=False)  # 注意这个parse接收的是字符串
#                 time.sleep(3)  # 定时发起请求，此时程序不会停止！
#
#     def parse(self, response):
#         print(response.url)
#         yield Item(response.url)  # 一定要写yield
