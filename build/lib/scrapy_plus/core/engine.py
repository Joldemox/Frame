# 引擎调度的流程

from scrapy_plus.conf import settings

if settings.ASYNC_TYPE == 'thread':
    # 线程池
    from multiprocessing.dummy import Pool
elif settings.ASYNC_TYPE == 'coroutine':
    # 自定义协程
    # 此处的导入文件不能使用async，原因不知道，可能是内部定好的方法
    from scrapy_plus.self_async.coroutine import Pool
else:
    raise Exception('don`t  support this way:{}'.format(settings.ASYNC_TYPE))

# 导入4大模块
from .scheduler import Scheduler
from .downloader import Downloader
import importlib
import time

from scrapy_plus.http.request import Request
from scrapy_plus.utils.log import logger
from datetime import datetime
from scrapy_plus.utils.collector import NormalStatsCollector, RedisStatsCollector


class Engine(object):
    def __init__(self):
        if settings.IS_DISTRIBUTE:
            self.collector = RedisStatsCollector()
        else:
            self.collector = NormalStatsCollector()
        self.scheduler = Scheduler(self.collector)

        # 实例化四个对象
        self.spiders = self._auto_import_instances(settings.SPIDERS, isspider=True)
        # self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipelines = self._auto_import_instances(settings.PIPELINES)

        # 实例化中间件
        self.spider_mids = self._auto_import_instances(settings.SPIDERS_MIDDLEWARES)
        self.down_mids = self._auto_import_instances(settings.DOWNLOADER_MIDDLEWARES)

        # # 记录请求个数和响应个数
        # self.total_request_num = 0
        # self.total_response_num = 0

        # 创建线程池
        self.pool = Pool()
        # 允许递归
        self.is_running = True

    # 动态导包多方法
    def _auto_import_instances(self, path=[], isspider=False):
        '''通过配置文件，动态导入类并实例化
        path: 表示配置文件中配置的导入类的路径
        isspider: 由于爬虫需要返回的是一个字典，因此对其做对应的判断和处理
        '''
        instances = {} if isspider else []
        for p in path:
            module_name = p.rsplit(".", 1)[0]  # 取出模块名称
            cls_name = p.rsplit(".", 1)[1]  # 取出类名称
            ret = importlib.import_module(module_name)  # 动态导入爬虫模块
            cls = getattr(ret, cls_name)  # 根据类名称获取类对象

            if isspider:
                instances[cls.name] = cls()  # 组装成爬虫字典{spider_name:spider(),}
            else:
                instances.append(cls())  # 实例化类对象
                # 把管道中间件分别组装成 管道列表=[管道类1(),管道类2()] / 中间件列表 = [中间件类1(),中间件类2()]
        return instances  # 返回类对象字典或列表

    # 初始化请求对象：入队列
    def _start_requests(self):
        # 1、spider---request--->engine
        def _func(spider_name, spider):
            requests = spider.start_requests()

            for request in requests:
                # 爬虫中间件---request
                for spider_mid in self.spider_mids:
                    request = spider_mid.process_request(request)

                # 给对应的请求对象request绑定自己的爬虫key(可以动态绑定，即为如下)
                request.spider_name = spider_name

                # 2、engine---request--->scheduler
                self.scheduler.add_request(request)
                # 记录请求对象个数
                # self.total_request_num += 1
                self.collector.incr(self.collector.request_nums_key)

        for spider_name, spider in self.spiders.items():
            # 让每一个爬虫都异步执行初始化请求对象：入队列
            self.pool.apply_async(_func, args={spider_name, spider})

    # 出队列：下载数据
    def execute_request_response_item(self):
        # 3、scheduler---request--->engine
        request = self.scheduler.get_request()
        # 1、判断对象是否为空。2、跳出死循环
        if request is None:
            return

        # 下载中间件---resuqest
        for down_mid in self.down_mids:
            request = down_mid.process_request(request)
        # 4、engine---request--->downloader
        # 5、downloader---response--->engine
        response = self.downloader.get_response(request)

        # 将request的meta传递给response中的meta
        response.meta = request.meta

        # 下载中间件---response
        for down_mid in self.down_mids:
            response = down_mid.process_response(response)

        # 爬虫中间件---response
        for spider_mid in self.spider_mids:
            response = spider_mid.process_response(response)
        # 6、engine---response--->spider

        # 使用字典之后，只需要对应解析爬虫名称就能对应解析方法
        # 所以之后的爬虫方法不再需要遍历
        spider = self.spiders[request.spider_name]

        # 根据当前爬虫自己的请求对象，生成对应的解析方法，并引用于之后的解析
        # for spider in self.spiders:
        parse = getattr(spider, request.parse)
        results = parse(response)

        for result in results:
            # 7、result---engine判断
            if isinstance(result, Request):
                # 对于新的请求对象也要绑定key
                result.spider_name = request.spider_name

                # 如果是request：engine---request--->scheduler
                # 如果是新请求，需要重新进入爬虫中间件
                for spider_mid in self.spider_mids:
                    result = spider_mid.process_request(result)
                self.scheduler.add_request(result)

                # 注意点：新的请求对象记录个数
                # 因为新的请求对象已经进入了队列，而引擎却没有进行加一的计数
                # self.total_request_num += 1
                self.collector.incr(self.collector.request_nums_key)
            else:
                # 如果是item:engine---item--->pipeline
                for pipeline in self.pipelines:
                    pipeline.process_item(result, spider)

        # 记录响应对象个数
        # self.total_response_num += 1
        self.collector.incr(self.collector.response_nums_key)

    # 构建进程池中的回调函数：递归
    def _callback(self, item):
        if self.is_running:
            self.pool.apply_async(self.execute_request_response_item, callback=self._callback,
                                  error_callback=self._error_back)

    # 捕获子线程异常
    def _error_back(self, e):
        # print(e)
        logger.exception(e)
        raise e

    def _start(self):
        '''调度4个模块'''
        # 加入线程池
        self.pool.apply_async(self._start_requests, error_callback=self._error_back)

        # 应该手动设置最大并发数
        for i in range(5):
            # 此中的异步方法中，传入的target是一个函数名称而不是一个方法，所以不能在后面加括号
            self.pool.apply_async(self.execute_request_response_item, callback=self._callback,
                                  error_callback=self._error_back)

        # 判断多爬虫中，没有增量式的条件
        sum_task = sum([spider.time_task for spider in self.spiders.values()])

        while True:
            time.sleep(0.001)
            # self.pool.apply_async(self.execute_request_response_item())
            # 只有当值为0，即为没有增量式才会退出
            if sum_task == 0:
                # 由于异步的问题，所以需要加入条件阻塞
                if self.collector.request_nums != 0:
                    # 判断退出条件，爬虫结束
                    if self.collector.response_nums + self.collector.repeat_request_nums >= self.collector.request_nums:
                        self.is_running = False
                        break

        self.pool.close()
        self.pool.join()

    # 将上面的调度方法变成私有方法，进行嵌套，方便日志记录时间
    def start(self):
        start_time = datetime.now()
        self._start()
        end_time = datetime.now()

        logger.info('this is a distribute spider:{}'.format(settings.IS_DISTRIBUTE))
        logger.info('the self_async is {}'.format(settings.ASYNC_TYPE))
        logger.info('the spider start at {}'.format(start_time))
        logger.info('the spider end in {}'.format(end_time))
        logger.info("the request's total is {}".format(self.collector.request_nums))
        logger.info("the repetitive request's total is {}".format(self.collector.repeat_request_nums))
        logger.info("the response's total is {}".format(self.collector.response_nums))
        logger.info('the spider pass with {}'.format((end_time - start_time).total_seconds()))

        # 清空redis中记录的个数
        self.collector.clear()
