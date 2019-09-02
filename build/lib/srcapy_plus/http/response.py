'''
自定义响应对象
url,code,headers,request,body,
'''


class Response(object):
    def __init__(self, url, code, headers, request, body, ):
        self.url = url
        self.code = code
        self.headers = headers
        self.request = request
        self.body = body
