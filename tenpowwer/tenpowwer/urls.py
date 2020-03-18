"""tenpowwer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url , include
from django.contrib import admin

import article

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 头条
    url(r'^', include('article.urls')),
    # 问答
    url(r'^', include('question.urls')),
    # 用户
    url(r'^', include('users.urls')),
    # 招聘
    url(r'^', include('recruit.urls')),
    # 吐槽
    url(r'^', include('spit.urls')),
]
