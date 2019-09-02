'''
自定义类型
'''


class Item(object):
    def __init__(self, data):
        self._data = data

    @property
    # 私有属性，防止被修改，也可以不加装饰器
    def data(self):
        return self._data