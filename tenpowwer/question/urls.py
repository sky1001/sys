
from django.conf.urls import url
from rest_framework import routers

from question.views import QuestionViewSet
from . import views

router = routers.SimpleRouter()
router.register(r'questions', QuestionViewSet, base_name='question')
router.register(r'reply', views.ReplyViewSet)
router.register(r'labels', views.LabelsViewSet,base_name='labels')
urlpatterns = [
# url(r'^articles//$', views.LabelsViewSet.as_view())
]
urlpatterns += router.urls
