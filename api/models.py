from django.db import models
#
# class UserInfo(models.Model):
#     username = models.CharField(max_length=32, unique=True) #unique 唯一索引
#     password= models.CharField(max_length=64)
#
#
# class UserToken(models.Model):
#     user = models.OneToOneField(to='UserInfo', on_delete=None)#这个用来关联上面那张userinfo
#     token = models.CharField(max_length=64)
#     time = models.CharField(max_length=64)
#
#
# class IpInfo(models.Model):
#     ip = models.CharField(max_length=32)
#     time = models.CharField(max_length=64)
#
#
#
# class PicTest(models.Model):
#
#     goods_pic = models.ImageField(upload_to='api')