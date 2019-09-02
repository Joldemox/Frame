'''
传递数据
'''


class Pipline(object):
    def process_item(self, item):
        print('piplines:{}'.format(item.data))
        return item