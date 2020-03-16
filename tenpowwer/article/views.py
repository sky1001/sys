from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

from article.mixin import MeiduoPagination
from article.models import Channel, Article
# Create your views here.
from rest_framework.viewsets import ModelViewSet

from article.serialzers import  ChannelsSerializers, ArticleSerializerForList



class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    # serializer_class = ArticleSerializers
    pagination_class = MeiduoPagination# 按频道获取文章列表 /article/{pk}/channel/
    @action(methods=['get'], detail=True, url_path="channel")
    def get_article_by_channel(self, request, pk):
        if pk == "-1":
            articles = self.get_queryset()
        else:
            channel = Channel.objects.get(id=pk)
            articles = self.get_queryset().filter(channel=channel)

        page = self.paginate_queryset(articles)
        if page is not None:
            s = ArticleSerializerForList(page, many=True)
            return self.get_paginated_response(s.data)
        else:
            s = ArticleSerializerForList(instance=articles, many=True)
            return Response(s.data)
    # 收藏和取消收藏
    # @action(methods=['PUT'],detail=True,url_path='collect')
    # def get_article_by_collect(self,request,pk):

class ChannelsViews(ModelViewSet):
    queryset =Channel.objects.all()
    serializer_class = ChannelsSerializers
    pagination_class = MeiduoPagination