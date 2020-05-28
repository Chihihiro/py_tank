"""py_tank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views as apiviews
from django.conf.urls import url, include
urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^api/v1/auth/$', apiviews.AuthView.as_view()),
    # url(r'^api/v1/ip/$', apiviews.IpView.as_view()),
    url(r'^api/', include('api.urls')),
]
