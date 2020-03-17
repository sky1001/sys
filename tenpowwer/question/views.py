from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# Create your views here.
from question.models import Question
from question.serializers import  QueationSerializerForCreate


class QuestionViewSet(ModelViewSet):
    # 重写create方法
    def create(self, request, *args, **kwargs):
        try:
            user = request.user
        except:
            user = None
        if user is not None or user.is_is_authenticated:
            data = request.data
            data['user']=user.id
            ser = QueationSerializerForCreate(data=data)
            ser.is_valid(raise_exception=True)
            ser.save()
            return Response(ser.data)
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)
    # 最新回答
    @action(methods=['get'],detail=True,url_path='label/new')
    def question_by_new(self,request,pk):
        # 获取用户
        question = Question.objects.order_by('-create_time')
        # page = self.paginate_queryset(question)
        s = QueationSerializerForCreate(instance=question,many=True)
        return Response(s.data)
    # 热门回答
    @action(methods=['get'], detail=True, url_path='label/new')
    def question_by_new(self, request, pk):
        # 获取用户
        question = Question.objects.order_by('visits')
        # page = self.paginate_queryset(question)
        s = QueationSerializerForCreate(instance=question, many=True)
        return Response(s.data)