# 下载中间件
class DownloaderMiddlewareOne(object):
    # 传递request
    def process_request(self, request):
        # print('下载中间件---request')
        return request

    # 传递response
    def process_response(self, response):
        # print('下载中间件---response')
        return response


class DownloaderMiddlewareTwo(object):
    # 传递request
    def process_request(self, request):
        # print('下载中间件---request')
        return request

    # 传递response
    def process_response(self, response):
        # print('下载中间件---response')
        return response