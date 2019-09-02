'''
下载数据,发出请求方式：
urllib.request
requests
urllib2
'''

import requests
from scrapy_plus.http.response import Response

from scrapy_plus.utils.log import logger


class Downloader(object):
    def get_response(self, request):
        # 判断请求方式
        if request.method == 'GET':
            # 使用第三方request是获取的response，不是自定义的response对象类型
            response = requests.get(request.url, headers=request.headers, params=request.params)
        elif request.method == 'POST':
            response = requests.post(request.url, headers=request.headers, data=request.data)
        else:
            raise Exception('Not support the way of "{}", please use "GET" or "POST" to request.'.format(request.method))

        # 将下载的数据返回给引擎
        return Response(
            url=response.url,
            headers=response.headers,
            request=request,
            body=response.content,
            code=response.status_code,
            meta={}
        )