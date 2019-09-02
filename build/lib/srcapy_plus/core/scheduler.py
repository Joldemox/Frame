'''
自定义调度器
1、入队列，2、出队列，3、去重
'''

# six作为第三方库，可以直接适配PY2和PY3
from six.moves.queue import Queue


class Scheduler(object):
    def __init__(self):
        # 初始化队列
        self.queue = Queue()

    # 1、入队列
    def add_request(self, request):
        self.queue.put(request)

    # 2、出队列
    def get_request(self):
        return self.queue.get()

    # 3、去重
    def filter_request(self, request):
        pass
