from rest_framework.authentication import BaseAuthentication
import time
from api import models

from rest_framework import exceptions
import re

# 创建一个我的认证类 继承BaseAuthentication方法
class MyAuthtication(BaseAuthentication):
    # 设置内置authenticate重写authenticate这个方法
    def authenticate(self, request):
        # 将用户输入的token用变量接收
        # token = request._request.GET.get('token')
        token = request.query_params.get('token')
        print(token)
        # 然后在数据库进行匹配
        token_obj = models.UserToken.objects.filter(token=token).first()
        # 如果认证失败
        print('token_obj', token_obj)
        if not token_obj:
            # 就返回失败
            raise exceptions.AuthenticationFailed("用户认证失败")
        # 在 rest framework内部 会将这两个字段赋值给request,以供后续操作使用
        now = int(time.time())
        tt = int(token_obj.time)
        #下面那个是6个小时过期的判断
        if now > (tt + 60*60*6):  # 重点就在这句了，这里做了一个Token过期的验证，如果当前的时间大于Token创建时间+DAYS天，那么久返回Token已经过期
            raise exceptions.AuthenticationFailed('Token has expired')
        # 正确就返回用户和token
        print('token 正确')
        print(token_obj.user.user_type)#在下面权限认证方面可以找出它的user_type
        return (token_obj.user, token)


# 如果pass 就调用原有的方法
class MyAuthtication_None(BaseAuthentication):
    def authenticate(self, request):
        pass
