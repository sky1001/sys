import json

import base64
from django import http
from django.conf import settings
from django.shortcuts import render
from django.views import View
from rest_framework.decorators import action
from rest_framework.response import Response

from article.mixin import MeiduoPagination
from article.models import Channel, Article
# Create your views here.
from rest_framework.viewsets import ModelViewSet

from article.serialzers import  ChannelsSerializers, ArticleSerializerForList, LabelsSerializer, \
    ArticleSerializerForCreate
from question.models import Label
# 上传图片
# from tenpowwer import settings
from tenpowwer.settings import FDFS_BASE_URL
# from article.serializers import ArticleSerializerForCreate,


class UploadViews(View):
    def post(self,request):
        # 获取图片的数据
        data = request.FILES.get('img')
        # 3.上传图片 fdfs
        # 链接 fastdfs

        from fdfs_client.client import Fdfs_client
        client = Fdfs_client(settings.FASTDFS_PATH)
        # 上传图片到fastDFS
        res = client.upload_by_buffer(data.read())
        # 判断是否上传成功
        if res['Status'] != 'Upload successed.':
            return Response(status=403)
        # 获取url地址
        image_url = res['Remote file_id']
        image_url = FDFS_BASE_URL+image_url
        return http.JsonResponse({
            'imgurl':image_url
        })


class LabelsViews(ModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelsSerializer

class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializerForList
    # pagination_class = MeiduoPagination# 按频道获取文章列表 /article/{pk}/channel/
    # 新建文章 /article/
    # 新建文章 /article/
    def create(self, request, *args, **kwargs):

        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            request_params = request.data
            request_params['user'] = user.id
            serializer = ArticleSerializerForCreate(data=request_params)
            serializer.request = request
            serializer.is_valid(raise_exception=True)
            article = serializer.save()
            return Response({'success': True, 'message': '发表成功', 'articleid': article.id})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)
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

    # # 文章列表
    def list(self, request, *args, **kwargs):
        articles = super().get_queryset()
        s = ArticleSerializerForList(instance=articles, many=True)
        return Response(s.data)
    # 收藏和取消收藏
    # @action(methods=['PUT'],detail=True,url_path='collect')
    # def get_article_by_collect(self,request,pk):

class ChannelsViews(ModelViewSet):
    queryset =Channel.objects.all()
    serializer_class = ChannelsSerializers
    pagination_class = MeiduoPagination