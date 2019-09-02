# 爬虫中间件
class SpiderMiddlewareOne(object):
    # 传递request
    def process_request(self, request):
        # print('爬虫中间件---request')
        return request

    # 传递response
    def process_response(self, response):
        # print('爬虫中间件---response')
        return response


class SpiderMiddlewareTwo(object):
    # 传递request
    def process_request(self, request):
        # print('爬虫中间件---request')
        return request

    # 传递response
    def process_response(self, response):
        # print('爬虫中间件---response')
        return response