from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from api.views import *

# router = routers.DefaultRouter()
# router.register(r'xxxx', apiviews.V1View)

urlpatterns = [
    # path('admin/', admin.site.urls),
    # url(r'^api/v1/auth/$', AuthView.as_view()),
    # url(r'^api/v1/order/$', OrderView.as_view()),
    # url(r'^(?P<version>\w+)/auth/$', AuthView.as_view()),
    # url(r'^(?P<version>\w+)/order/$',  OrderView.as_view()),
    # url(r'^(?P<version>\w+)/ip/$',  IpView.as_view()),
    # url(r'^(?P<version>\w+)/login/$',  LoginView.as_view()),
    # url(r'^login/$',  LoginView.as_view()),
    # url(r'^class/page(?P<page>\d+)/(?P<type>.*?)/(?P<user>.*?)/(?P<num>.*?)/$',  ClassView.as_view()),
    # url(r'^index/page(?P<page>\d+)/(?P<type>.*?)/(?P<num>.*?)/$',  IndexView.as_view()),
    url(r'^index/',  Index2View.as_view()),
    url(r'^class/',  Class2View.as_view()),
    # url(r'^class3/page(?P<page>\d+)/(?P<type>.*?)$',  ClassView3.as_view()),






]