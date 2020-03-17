
from django.conf.urls import url
from rest_framework import routers

from question.views import QuestionViewSet
from . import views

router = routers.SimpleRouter()
router.register(r'questions', QuestionViewSet, base_name='question')
urlpatterns = [
    # url(r'^/$', views.aa.as_view()),
]
urlpatterns += router.urls
