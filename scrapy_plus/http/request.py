'''
自定义请求对象
url,method,headers,cookies,
'''


class Request(object):
    def __init__(self,
                 url,
                 method='GET',
                 headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'},
                 cookies={},
                 params={},
                 data={},
                 parse='parse',
                 meta={},
                 # spider_name='',
                 filter = True
                 ):
        self.url = url
        self.method = method
        self.headers = headers
        self.cookies = cookies
        self.params = params
        self.data = data

        # 多解析函数
        self.parse = parse
        self.meta = meta
        # self.spider_name = spider_name

        # 添加增量式，url不更新仍然爬取数据,默认是True，去重的
        self.filter = filter
