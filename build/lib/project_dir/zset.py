import redis

from scrapy_plus.http.request import Request
import pickle

if __name__ == '__main__':
    # 在redis中，只能左进右出
    client = redis.StrictRedis()
    key = 'FIFO'
    # print(client.rpop(key))
    # # 序列化
    # request = Request('http://www.baidu.com')
    # # client.lpush(key, request.url)
    # # print(client.rpop(key))
    #
    # # 入队列前序列化成二进制
    # request = pickle.dumps(request)
    # client.lpush(key, request)
    # result = client.rpop(key)
    # # print(result)
    # # 出队列，反序列化成对象
    # result = pickle.loads(result)
    # print(result.url)

    # 去重
    # client.sadd(key, '1')
    result = client.sismember(key, 1)
    print(result)