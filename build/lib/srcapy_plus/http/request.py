'''
自定义请求对象
url,method,headers,cookies,
'''


class Request(object):
    def __init__(self, url, method='GET', headers={}, cookies={}, params={}, data={}):
        self.url = url
        self.method = method
        self.headers = headers
        self.cookies = cookies
        self.params = params
        self.data = data