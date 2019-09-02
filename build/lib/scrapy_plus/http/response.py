'''
自定义响应对象
url,code,headers,request,body,
'''
from lxml import etree
from bs4 import BeautifulSoup
import re
import json

class Response(object):
    def __init__(self, url, code, headers, request, body, meta, ):
        self.url = url
        self.code = code
        self.headers = headers
        self.request = request
        self.body = body

        # 源码既在响应对象中传递，所以现在选择在引擎中传递meta
        # self.meta = self.request.meta
        self.meta = meta

    '''自定义方法'''
    # 1、xpath
    def xpath(self, rule):
        # 转换解析类型
        html_data = etree.HTML(self.body)
        # 调用xpath解析方法
        return html_data.xpath(rule)

    # 2、bs4
    def select(self, selector):
        # 转换类型
        soup = BeautifulSoup(self.body, 'lxml')
        # select解析
        return soup.select(selector)

    # 3、re
    def re_find(self, pattern):
        if self.body:
            return re.findall(pattern, self.body)
        else:
            return None

    # 4、json，requests中存在json的方法。如果返回的数据是json字符串，就进行解析
    @property
    def json(self):
        try:
            data = json.loads(self.body.decode())
            return data
        except:
            return None