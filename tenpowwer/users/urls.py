
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    # 发送短信
    url(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SmsView.as_view()),

    # 注册
    url(r'^users/$', views.CreateUserView.as_view()),

    # 登录
    url(r'^authorizations/$', obtain_jwt_token),

    # 用户详细信息
    url(r'^user/$', views.UserListView.as_view()),
]
