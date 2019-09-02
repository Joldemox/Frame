'''
爬虫测试文件
'''

from scrapy_plus.core.engine import Engine

if __name__ == '__main__':
    # 实例化引擎对象
    engine = Engine()
    # 开启引擎
    engine.start()

