import time
from rest_framework.throttling import BaseThrottle

VISIT_RECORD = {}

class VisitThrottle(BaseThrottle):

    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        # addr = self.get_ident(request)
        # 这下面的是手写上面的调用Base_Throttle里面的获取IP方法
        addr = request.META.get('REMOTE_ADDR')

        ctime = time.time()
        if addr not in VISIT_RECORD:
            VISIT_RECORD[addr] = [ctime, ]

        history = self.history = VISIT_RECORD.get(addr)
        while history and history[-1] < ctime -10:
            history.pop()
        if len(history) <3:
            history.insert(0, ctime)
            print(history)
            return True

    def wait(self):
        now = time.time()
        last = self.history[-1]
        return 10 - (now -last)



from rest_framework.throttling import SimpleRateThrottle


class VisitThrottle2(SimpleRateThrottle):
    scope = 'LL'

    def get_cache_key(self, request, view):
        return self.get_ident(request)#这个是更具ip来限制


class VisitThrottle_User(SimpleRateThrottle):
    scope = 'User'

    def get_cache_key(self, request, view):
        return request.user.username#这个是通过账号来限制访问频率