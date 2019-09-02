# 引擎调度的流程

# 导入4大模块
from .spider import Spider
from .scheduler import Scheduler
from .downloader import Downloader
from .pipeline import Pipline

from scrapy_plus.http.request import Request


class Engine(object):
    def __init__(self):
        # 实例化四个对象
        self.spider = Spider()
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipeline = Pipline()

    def start(self):
        # 调度4个模块
        # 1、spider---request--->engine
        request = self.spider.start_request()

        # 2、engine---request--->scheduler
        self.scheduler.add_request(request)

        # 3、scheduler---request--->engine
        request = self.scheduler.get_request()

        # 4、engine---request--->downloader
        # 5、downloader---response--->engine
        response = self.downloader.get_response(request)

        # 6、engine---response--->spider
        result = self.spider.parse(response)

        # 7、result---engine判断
        if isinstance(result, Request):
            # 如果是request：engine---request--->scheduler
            self.scheduler.add_request(result)
        else:
            # 如果是item:engine---item--->pipeline
            self.pipeline.process_item(result)