
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^channels/$', views.ChannelsViews.as_view({'get': 'list'})),
]