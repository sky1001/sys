from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # url(r'^/$', views.aa.as_view()),
]

router = DefaultRouter()
# 热门城市
router.register(r'city', views.CityViewSet)
# 企业
router.register(r'enterprise', views.EnterpriseViewSet)
# 职位
router.register(r'recruits', views.RecruitViewSet)

urlpatterns += router.urls


