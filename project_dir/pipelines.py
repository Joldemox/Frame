# 多个管道
import redis


class BaiduPipeline(object):
    '''百度'''
    def __init__(self):
        self._redis = redis.StrictRedis()
        self.item_key = 'baidu_item'

    def process_item(self, item, spider):
        if spider.name == 'baidu':
            print('baidu:{}'.format(item.data))
            self._redis.lpush(self.item_key, item.data)
        return item


class DoubanPipeline(object):
    '''豆瓣'''

    def process_item(self, item, spider):
        if spider.name == 'douban':
            print('douban:{}'.format(item.data))
        return item
