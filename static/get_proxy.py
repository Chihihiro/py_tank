# -*- coding: utf-8 -*-
# @Time    : 2019/9/25 15:46
# @Author  : Chihiro

# -*- coding: utf-8 -*-
"""
IP代理池
受限于第三方代理的白名单
一个代理通道只支持3个访问IP白名单
"""

import redis
import socket



REDIS_SETTINGS = dict(
    host='10.10.53.221',
    port=6379,
    db=1,
    decode_responses=True,
)

# local = dict(
#     host='localhost',
#     port=6379,
#     db=3,
#     decode_responses=True,
# )


class pack_redis(object):

    def __init__(self, table_name):
        hostname = socket.gethostname()

        self.table_name = table_name
        if hostname in ('DESKTOP-6UPQ2C9', 'chihiro'):
            self.__client = redis.Redis(**REDIS_SETTINGS)
        else:
            # pass
            self.__client = redis.Redis(**REDIS_SETTINGS)

        self.__interval = 10

    @property
    def name(self):
        return self.table_name

    @property
    def interval(self):
        return self.__interval

    def put(self, *data):
        """ append proxy to pool."""
        self.__client.rpush(self.table_name, *data)

    def lpop(self):
        """ get one proxy from pool."""
        return self.__client.lpop(self.table_name)

    def flush(self):
        """ delete proxy pool."""
        self.__client.delete(self.table_name)


    def llen(self):
        """统计某个表元素个数"""
        return self.__client.llen(self.table_name)

    def get(self, count=1):
        """ get proxies range from left."""
        return self.__client.lrange(self.table_name, 0, count - 1)

    def trim(self, start, end):
        """ trim pool."""
        self.__client.ltrim(self.table_name, start, end)

    def __len__(self):
        return self.__client.llen(self.table_name)

    def lpush(self, ll):
        """传入list 或者str写入库操作"""
        if type(ll) is list:
            for i in ll:
                self.__client.lpush(self.table_name, i)
        else:
            self.__client.lpush(self.table_name, ll)

# a = pack_redis('ip_proxy1')
# b = a.lpop()
# print(b)

