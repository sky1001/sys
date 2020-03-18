import re

import jwt
from django.conf import settings
from django_redis import get_redis_connection
from rest_framework import serializers
from datetime import datetime,timedelta

from article.models import Article
from question.models import Label, Question, Reply
from recruit.models import Enterprise
from users.models import User

# 注册
class CreateUserSerializer(serializers.ModelSerializer):
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    token = serializers.CharField(label='token', read_only=True)
    class Meta:
        model = User
        fields = ['id','username','password','mobile','token','avatar','sms_code']
        extra_kwargs = {
            'username': {
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '用户名为6-20个字符!',
                    'max_length': '用户名为6-20个字符!',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 6,
                'max_length': 20,
                'error_messages': {
                    'min_length': '密码为6-20个字符',
                    'max_length': '密码为6-20个字符',
                }
            }
        }
    def validate_mobile(self,value):
        print(value)
        if not re.match(r'^1[345789]\d{9}$',value):
            raise serializers.ValidationError('手机格式不正确')
        return value
    def validate(self, attrs):
        # 链接redis数据库
        sms_redis_client = get_redis_connection('sms_code')
        # 取出mobile
        mobile = attrs.get('mobile')
        print(mobile)
        # 取出验证码
        mobile_redis = sms_redis_client.get("sms_%s" % mobile)
        # 取出验证码
        sms = attrs.get('sms_code')
        print(mobile_redis)
        if mobile_redis is None:
            raise serializers.ValidationError('验证码失效')
        if sms != mobile_redis.decode():
            raise serializers.ValidationError('验证码错误')
        return attrs

    def create(self, validated_data):
        del validated_data['sms_code']
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        print(user.mobile)
        user.save()
        # 3.设置载体
        payload = {
            "user_id": user.id,
            "username": user.username,
            # 设置过期时间
            'exp': datetime.utcnow() + timedelta(hours=1)
        }

        # 4.加密
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        user.token = token
        return user

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields =["id", "label_name"]


class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    labels = serializers.StringRelatedField(read_only=True,many=True)
    class Meta:
        model = Question
        fields = ["id","createtime","labels","reply","replyname","replytime","title","unuseful_count","useful_count","user","visits"]

class ReplySerializer(serializers.ModelSerializer):
    user = CreateUserSerializer(read_only=True)
    class Meta:
        model = Reply
        fields = ["id", "content","createtime","useful_count",'problem',"unuseful_count","user"]

class ArticleSerializer(serializers.ModelSerializer):
    user = CreateUserSerializer(read_only=True)
    collected = serializers.BooleanField(default=False)
    class Meta:
        model = Article
        fields = ("id", "title","content","createtime","user","collected_users","collected","image","visits")

class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ('id', 'name','labels','logo','recruits','summary')

# 个人中心
class UserListSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(required=False, many=True)
    username = serializers.CharField(read_only=True)
    questions = QuestionSerializer(read_only=True, many=True)
    answer_question = ReplySerializer(read_only=True, many=True)
    collected_articles = ArticleSerializer(read_only=True, many=True)
    enterpises = EnterpriseSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'mobile', 'avatar','labels','questions','answer_question','collected_articles','enterpises']

# 修改密码
class UserUpdatePwdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


# 修改擅长技术
class UpdateLabelSerializer(serializers.ModelSerializer):
    labels = serializers.PrimaryKeyRelatedField(required=True, many=True,queryset=Label.objects.all())
    class Meta:
        model = User
        fields = ('id','labels')

