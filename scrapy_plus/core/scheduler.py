'''
自定义调度器
1、入队列，2、出队列，3、去重
'''

from scrapy_plus.conf import settings

if settings.IS_DISTRIBUTE:
    # 分布式
    from scrapy_plus.utils.queue import Queue
else:
    # 非分布式
    from six.moves.queue import Queue

# six作为第三方库，可以直接适配PY2和PY3
# from six.moves.queue import Queue
from scrapy_plus.utils.log import logger
import hashlib
import w3lib.url
import six
from scrapy_plus.utils.set import NormalFilterContainer, RedisFilterContainer


class Scheduler(object):
    def __init__(self, collector):
        # 让引擎判断是否为分布式
        self.collector = collector

        # 过滤器的判断
        if settings.IS_DISTRIBUTE:
            self.filter_container = RedisFilterContainer()
        else:
            self.filter_container = NormalFilterContainer()

        # 初始化队列
        self.queue = Queue()

        # # 记录重复请求个数
        # self.total_repeat_num = 0

    # 1、入队列
    def add_request(self, request):
        # 在入队列前便生成指纹
        # 根据请求对象生成指纹进行比对
        fp = self._create_fp(request)

        if request.filter:
            # 过滤
            # 直接根据指纹进行判断
            if not self.filter_request(fp):
                # 表示不重复，添加新多请求对象并入队列
                self.queue.put(request)
                # 不再将url进入队列，而是直接进入指纹，方便去重判定
                self.filter_container.add_fp(fp)
            else:
                logger.info('this is a repetitive request:{}'.format(request.url))
                # self.total_repeat_num += 1
                self.collector.incr(self.collector.repeat_request_nums_key)
        else:
            # 过滤，直接入队列
            self.queue.put(request)
            logger.info('a repetitive request is added in queue:{}'.format(request.url))

        # # 直接根据指纹进行判断
        # if not self.filter_request(fp):
        #     # 表示不重复，添加新多请求对象并入队列
        #     self.queue.put(request)
        #     # 不再将url进入队列，而是直接进入指纹，方便去重判定
        #     self.filter_container.add_fp(fp)
        # else:
        #     logger.info('this is a repetitive request:{}'.format(request.url))
        #     # self.total_repeat_num += 1
        #     self.collector.incr(self.collector.repeat_request_nums_key)

    # 2、出队列
    def get_request(self):
        try:
            # 队列为空时，会阻塞，既不会出现死循环
            # 所以需要改为非阻塞
            return self.queue.get(False)
        except:
            return None

    # 3、去重
    def filter_request(self, fp):
        # if fp in self.filter_container:
        #     return True
        # else:
        #     return False
        return self.filter_container.exists(fp)

    # 根据请求对象，创建指纹
    def _create_fp(self, request):
        # url排序
        url = w3lib.url.canonicalize_url(request.url)

        # method大小写,统一给为大写
        method = request.method.upper()

        # params、data中的参数排序
        params = sorted(request.params.items())
        data = sorted(request.data.items())

        # 拼接指纹字符串
        fp_str = url + method + str(params) + str(data)

        # 生成指纹
        fp = hashlib.sha1()
        fp.update(fp_str.encode())
        return fp.hexdigest()

    # 在之前的判定中已经写过，写在这里是方便代码的管理
    def _to_bytes(self, string):
        """为了兼容py2和py3，利用_to_bytes方法，把所有的字符串转化为字节类型"""
        if six.PY2:
            if isinstance(string, str):
                return string
            else:  # 如果是python2的unicode类型，转化为字节类型
                return string.encode('utf-8')
        elif six.PY3:
            if isinstance(string, str):  # 如果是python3的str类型，转化为字节类型
                return string.encode("utf-8")
            else:
                return string
