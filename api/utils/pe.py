from rest_framework.permissions import BasePermission
from api import models
from rest_framework import exceptions

class MyPermission(BasePermission):#BasePermission是规范必须要继承 其实不继承也能跑
    """
    推荐使用下面2个 这个的是用账户密码来判断的
    """
    message = '必须是SVIP才行'
    def has_permission(self, request, view):
        # print('必须是SVIP才行')
        user = request._request.GET.get('username')
        password = request._request.GET.get('password')
        print(user)
        obj = models.UserInfo.objects.filter(username=user, password=password).first()
        if obj:
            user_type = models.UserInfo.objects.get(username=user).user_type
            print(user_type)
            if user_type != 3:
                return False
            return True
        else:
            raise exceptions.AuthenticationFailed('用户认证失败111账号或密码错误')

class MyPermission1(BasePermission):
    message = '必须是SVIP才行'
    def has_permission(self, request, view):
        if request.user.user_type != 3:
            return False
        return True

class MyPermission2(BasePermission):
    message = '必须是SVIP才行'
    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return False
        return True