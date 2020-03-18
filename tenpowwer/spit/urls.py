from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    # url(r'^/$', views.aa.as_view()),
]

router = DefaultRouter()
# 吐槽
router.register(r'spit', views.SpitViewSet)

urlpatterns += router.urls

