# 自定义协程，添加close和errorback方法

# 协程池
# 必须导入在最上面，因为协程池中改来socket模块
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool as BasePool


class Pool(BasePool):
    # errorback
    def apply_async(self, func, args=(), kwds={}, callback=None,
                    error_callback=None):
        return super().apply_async(func, args=args, kwds=kwds, callback=callback)

    # close
    def close(self):
        pass