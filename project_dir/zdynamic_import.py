# 动态导包
import importlib


def import_lib_dynamic(path_list, isspider=False):
    if isspider:
        result = {}
    else:
        result = []

    for path in path_list:
        # 截取字符串
        # class_name = path[path.rfind('.') + 1:]
        # module_name = path[:path.rfind('.')]
        module_name, class_name = path.rsplit(".", 1)

        # 根据字符串来动态导包，实例化对象
        # getattr(cls,'')
        mod = importlib.import_module(module_name)  # 动态导入爬虫模块
        cls = getattr(mod, class_name)  # 根据类名称获取类对象

        if isspider:
            result[cls().name] = cls()
        else:
            result.append(cls())

        print(result)


if __name__ == '__main__':
    # 多爬虫
    SPIDERS = [
        'spiders.baidu.BaiduSpider',
        # 'spiders.douban.DoubanSpider',
    ]

    # 多管道
    PIPELINES = [
        'pipelines.BaiduPipeline',
        # 'pipelines.DoubanPipeline',
    ]
    import_lib_dynamic(SPIDERS, isspider=True)
    import_lib_dynamic(PIPELINES)