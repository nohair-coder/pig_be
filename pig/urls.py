"""pig URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token

from apps.feeding_records.views import FeedingDataView
from apps.feeding_set.views import FeedingSetView
from apps.pig_base.views import PigBaseView
from apps.station.views import StationView, HandleStationView
from apps.user.views import UserViewset

from apps.WLAN_4G import views
router = DefaultRouter()
# 配置用户的url
router.register(r'user', UserViewset, basename='UserViewset')


urlpatterns = [
    path('admin/', admin.site.urls),

    re_path('^', include(router.urls)),
    # 测试token
    path('api-token-auth/', obtain_auth_token),
    # jwt的登录认证接口
    path(r'login/', obtain_jwt_token),

    # 以上接口不要改动，系统自带
    # 以下接口则是开发接口

    # 下位机采食量接口
    path('feedingdata/', FeedingDataView.as_view()),

    path(r'station/', StationView.as_view()),
    path(r'handlestation/', HandleStationView.as_view()),
    path(r'pigbase/', PigBaseView.as_view()),
    path(r'feedingset/', FeedingSetView.as_view()),
]
