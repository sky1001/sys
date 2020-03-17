
from django import http
from django.conf import settings
from django.views import View
from rest_framework.decorators import action
from rest_framework.response import Response
from article.mixin import MeiduoPagination
from article.models import Channel, Article,Comment
# Create your views here.
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet

from article.serialzers import  ChannelsSerializers, ArticleSerializerForList, LabelsSerializer, \
    ArticleSerializerForCreate,CommentSerializer,ArticleSerializerForDetail,CommentSerializerForCreate
from question.models import Label
# 上传图片
# from tenpowwer import settings
from tenpowwer.settings import FDFS_BASE_URL
# from article.serializers import ArticleSerializerForCreate,
# 获取数据
class SearchViews(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializerForList
    pagination_class = MeiduoPagination
    def get_queryset(self):
        # 获取搜索内容
        text = self.request.query_params.get('text')
        # 查询内容
        atr = Article.objects.filter(title__contains=text)
        return atr

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
    pagination_class = MeiduoPagination# 按频道获取文章列表 /article/{pk}/channel/

    # 文章详情  /article/{id}/
    def retrieve(self, request, *args, **kwargs):
        article = super().get_object()
        article.visits += 1
        article.save()
        s = ArticleSerializerForDetail(instance=article)
        return Response(s.data)
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
    # 收藏和取消收藏
    @action(methods=['put'], detail=True, url_path="collect")
    def get_article_by_collect(self, request, pk):
        try:
            # 获取用户数据
            user = request.user
        except:
            user = None
        # 判断用户是否存在
        if user is not None or user.is_authenticated:
            art = self.get_object()
            # 用户存在
            if user in art.collected_users.all():
                art.collected_users.remove(user)
                art.save()
                return Response({'success': True, 'message': '取消收藏'})
            else:
                art.collected_users.add(user)
                art.save()
                return Response({'success': True, 'message': '收藏成功'})
    # # 文章列表
    def list(self, request, *args, **kwargs):
        articles = super().get_queryset()
        s = ArticleSerializerForList(instance=articles, many=True)
        return Response(s.data)
    @action(methods=['post'],detail=True,url_path='publish_comment')
    def get_artcle_by_publish_comment(self,request,pk):
        try:
            user = request.user
        except:
            user = None
        # 判断用户是否存在
        if user is not None or user.is_authenticated:
            # arti = self.get_object()
            # arti.comment_count+=1
            # arti.save()
            # qur = request.data
            # par = qur.pop('parent')
            # par= Comment.objects.get(pk=par)
            # qur['user']=user
            # qur['article'] = arti
            # qur['parent'] = par
            # com = Comment.objects.create(**qur)
            # ser = CommentSerializer(com)
            article = self.get_object()
            article.comment_count += 1
            article.save()
            request_params = request.data
            request_params['user'] = user.id
            request_params['article'] = article.id
            s = CommentSerializerForCreate(data=request_params)
            s.is_valid(raise_exception=True)
            s.save()
            return Response({'success': True, 'message': '评论成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)
    @action(methods=['get'],detail=True)
    def get_comment_by(self,request,pk):
        try:
            user = request.user
        except:
            user = None
        # 判断用户是否存在
        if user is not None or user.is_authenticated:
            articles = super().get_queryset()
            com = Comment.objects.filter(article=articles)
            return com
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)
class ChannelsViews(ModelViewSet):
    queryset =Channel.objects.all()
    serializer_class = ChannelsSerializers
    pagination_class = MeiduoPagination

