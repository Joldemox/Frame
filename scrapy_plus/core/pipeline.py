'''
传递数据
'''


class Pipeline(object):
    def process_item(self, item):
        print('pipelines:{}'.format(item.data))
        return item