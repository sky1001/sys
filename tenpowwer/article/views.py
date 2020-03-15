from django.shortcuts import render

from article.mixin import MeiduoPagination
from article.models import Channel
# Create your views here.
from rest_framework.viewsets import ModelViewSet

from article.serialzers import ArticleSerializers


class ChannelsViews(ModelViewSet):
    queryset =Channel.objects.all()
    serializer_class = ArticleSerializers
    pagination_class = MeiduoPagination