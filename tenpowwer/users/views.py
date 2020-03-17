
from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


from users import serializers

# 短信验证码
class SmsView(APIView):
    def get(self,request,mobile):

        from random import randint
        sms_code = "%06d" % randint(0, 999999)
        # sms_code = randint(100000, 999999)
        print(sms_code)
        sms_redis_client = get_redis_connection('sms_code')

        # 1.取出标识
        send_flag = sms_redis_client.get('send_flag_%s' % mobile)
        # 2.判断标识
        if send_flag:
            return http.HttpResponseForbidden('短信发送频繁')

        # 1.实例化管道
        pipeline = sms_redis_client.pipeline()
        # 2.将任务添加管道
        pipeline.setex('send_flag_%s' % mobile, 60, 1)
        pipeline.setex("sms_%s" % mobile, 300, sms_code)
        # 3.实行管道'
        pipeline.execute()

        # 4.让第三方 容联云-给手机号-发送短信
        from celery_tasks.sms.tasks import ccp_send_sms_code
        ccp_send_sms_code.delay(mobile, sms_code)

        # 5.告诉前端短信发送完毕
        return Response({'success':True,'sms_code':sms_code,'message':'OK'})

# 用户注册
class CreateUserView(CreateAPIView):
    serializer_class = serializers.CreateUserSerializer


