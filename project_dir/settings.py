# print('爬虫项目的settings文件')
import logging

# 断点续爬字段
FP_PERSIST = True

# 判断是否为分布式爬虫，默认为Fasle
# IS_DISTRIBUTE = False
IS_DISTRIBUTE = True

# redis数据库的配置
REDIS_QUEUE_NAME = 'redis_queu_key'
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_FP_KEY = 'redis_fp_key'


# 设置使用协程coroutine或是线程thread
ASYNC_TYPE = 'thread'
# ASYNC_TYPE = 'coroutine'

# 默认的日志配置
DEFAULT_LOG_LEVEL = logging.INFO  # 默认等级
DEFAULT_LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'  # 默认日志格式
DEFUALT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
DEFAULT_LOG_FILENAME = 'baidu.log'  # 默认日志文件名称

# 多爬虫
SPIDERS = [
    'spiders.baidu.BaiduSpider',
    'spiders.douban.DoubanSpider',
]

# 多管道
PIPELINES = [
    'pipelines.BaiduPipeline',
    'pipelines.DoubanPipeline',
]

# 爬虫中间件
SPIDERS_MIDDLEWARES = [
    'middlewares.spider_middleware.SpiderMiddlewareOne',
    # 'middlewares.spider_middleware.SpiderMiddlewareTwo',
]

# 下载中间件
DOWNLOADER_MIDDLEWARES = [
    'middlewares.downloader_middleware.DownloaderMiddlewareOne',
    # 'middlewares.downloader_middleware.DownloaderMiddlewareTwo',
]
