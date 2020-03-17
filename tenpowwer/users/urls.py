from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from users import views

from . import views

urlpatterns = [
    # 发送短信
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SmsView.as_view()),

    # 注册
    url(r'^users/$', views.CreateUserView.as_view()),

    # 1.使用 drf-jwt 实现返回token的登录功能
    url(r'^authorizations/$', obtain_jwt_token),
]
