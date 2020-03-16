
from django.conf.urls import url

from article.views import ArticleViewSet
from . import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'article', ArticleViewSet, base_name='article')
urlpatterns = [
    url(r'^channels/$', views.ChannelsViews.as_view({'get': 'list'})),
    # url(r'^article/(?P<id>\d)/channel/', views.AcView.as_view({'get': 'list'})),
]
urlpatterns += router.urls