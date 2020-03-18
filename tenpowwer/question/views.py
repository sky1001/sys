from django.shortcuts import render
from django_redis import get_redis_connection
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# Create your views here.
from question.models import Question, Reply
from question.serializers import  QueationSerializerForCreate,QuestionSerializerForDetail, RelySerializers


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    # serializer_class = QuestionSerializerForDetail
    # 详情
    # 查询问题详情 questions/{pk}/
    def retrieve(self, request, pk):
        question = self.get_object()
        question.visits += 1
        question.save()
        replies = question.replies.all()
        question.comment_question = []
        question.answer_question = []

        for item in replies:
            if item.type == 0:  # 问题的评论
                question.comment_question.append(item)
            elif item.type == 2:  # 回答的评论
                question.answer_question.append(item)

        s = QuestionSerializerForDetail(instance=question)
        return Response(s.data)
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
    @action(methods=["GET"], detail=True, url_path="label/new")
    def get_new_question_by_labelid(self, request, pk):
        # 获取用户
        question = Question.objects.all().order_by('-replytime')
        # page = self.paginate_queryset(question)
        s = QuestionSerializerForDetail(instance=question,many=True)
        return Response(s.data)
    # 热门回答
    @action(methods=['get'], detail=True, url_path='label/hot')
    def question_by_new(self, request, pk):
        # 获取用户
        question = Question.objects.all().order_by('visits')
        # page = self.paginate_queryset(question)
        s = QuestionSerializerForDetail(instance=question, many=True)
        return Response(s.data)
    # 等待回答
    @action(methods=['get'], detail=True, url_path='label/wait')
    def question_by_wait(self, request, pk):
        # 获取用户
        question = Question.objects.filter(reply=0).order_by('visits')
        # page = self.paginate_queryset(question)
        s = QuestionSerializerForDetail(instance=question, many=True)
        return Response(s.data)

    @action(methods=['put'], detail=True, url_path="unuseful")
    def question_by_unuserful(self, request, pk):
        # 判断用户是否存在
        try:
            user = request.user
        except:
            user = None
        if user is not None or user.is_is_authenticated:
            redis_conn = get_redis_connection('question')
            flag = redis_conn.hget("question_unuserful_%s" % user.id, pk)
            if flag:
                return Response({'success': False, 'message': '请不要重复操作'})
            # 获取问答的对象
            res = self.get_object()
            # 无用数加1
            res.unuseful_count += 1
            # 保存
            res.save()
            # 将数据存入redis数据库
            redis_conn.hset("question_unuserful_%s" % user.id, pk, user.id)
            return Response({'success': True, 'message': '操作成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)

    @action(methods=['put'], detail=True, url_path="useful")
    def question_by_userful(self, request, pk):
        # 判断用户是否存在
        try:
            user = request.user
        except:
            user = None
        if user is not None or user.is_is_authenticated:
            redis_conn = get_redis_connection('question')
            flag = redis_conn.hget("question_userful_%s" % user.id, pk)
            if flag:
                return Response({'success': False, 'message': '请不要重复操作'})
            # 获取问答的对象
            res = self.get_object()
            # 无用数加1
            res.useful_count += 1
            # 保存
            res.save()
            # 将数据存入redis数据库
            redis_conn.hset("question_userful_%s" % user.id, pk, user.id)
            return Response({'success': True, 'message': '操作成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)
class ReplyViewSet(ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = RelySerializers
    def create(self, request, *args, **kwargs):
        # 判断用户是否存在
        try:
            user = request.user
        except:
            user = None
        if user is not None or user.is_is_authenticated:
            re = request.data
            re['user'] = user.id
            ser = RelySerializers(data=re)
            ser.is_valid(raise_exception=True)
            reply = ser.save()
            problem = reply.problem
            if request.data.get('type') == 2:
                problem.reply += 1
                problem.replyname = reply.user.username
                problem.replytime = reply.createtime
                problem.save()
            return Response({'sucess':True,'message':'增加成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)
    @action(methods=['put'],detail=True,url_path="unuseful")
    def Reply_by_unuserful(self,request,pk):
        # 判断用户是否存在
        try:
            user = request.user
        except:
            user = None
        if user is not None or user.is_is_authenticated:
            redis_conn = get_redis_connection('question')
            flag = redis_conn.hget("reply_unuserful_%s" % user.id, pk)
            if flag:
                return Response({'success': False, 'message': '请不要重复操作'})
            # 获取问答的对象
            res = self.get_object()
            # 无用数加1
            res.unuseful_count += 1
            # 保存
            res.save()
            # 将数据存入redis数据库
            redis_conn.hset("reply_unuserful_%s" % user.id, pk,user.id)
            return Response({'success': True, 'message': '操作成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)
    @action(methods=['put'],detail=True,url_path="useful")
    def Reply_by_userful(self,request,pk):
        # 判断用户是否存在
        try:
            user = request.user
        except:
            user = None
        if user is not None or user.is_is_authenticated:
            redis_conn = get_redis_connection('question')
            flag = redis_conn.hget("reply_userful_%s" % user.id, pk)
            if flag:
                return Response({'success': False, 'message': '请不要重复操作'})
            # 获取问答的对象
            res = self.get_object()
            # 无用数加1
            res.useful_count += 1
            # 保存
            res.save()
            # 将数据存入redis数据库
            redis_conn.hset("reply_userful_%s" % user.id, pk,user.id)
            return Response({'success': True, 'message': '操作成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)

