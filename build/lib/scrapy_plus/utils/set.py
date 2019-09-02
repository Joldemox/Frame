# 适配分布式与非分布式过滤器
import redis
from scrapy_plus.conf import settings


class BaseFilter(object):
    # 添加到过滤器
    def add_fp(self, fp):
        pass

    # 判断重复的url
    def exists(self, fp):
        pass


# 非分布式
class NormalFilterContainer(BaseFilter):
    def __init__(self):
        self.filter_container = set()

    # 添加到过滤器
    def add_fp(self, fp):
        self.filter_container.add(fp)

    # 判断重复的url
    def exists(self, fp):
        if fp in self.filter_container:
            return True
        else:
            return False


# 分布式
class RedisFilterContainer(BaseFilter):
    def __init__(self):
        self.filter_container = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
        )
        # 保存指纹的key
        self.fp_key = settings.REDIS_FP_KEY

    # 添加到过滤器
    def add_fp(self, fp):
        self.filter_container.sadd(self.fp_key, fp)

    # 判断重复的url
    def exists(self, fp):
        # if fp in self.filter_container:
        #     return True
        # else:
        #     return False
        return self.filter_container.sismember(self.fp_key, fp)