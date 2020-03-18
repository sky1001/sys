from rest_framework import serializers
from rest_framework.response import Response

from article.models import Article, Comment
from users.models import User
from users.serializers import CreateUserSerializer


class ChannelsSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.StringRelatedField()

class ArticleSerializerForList(serializers.ModelSerializer):
    user = CreateUserSerializer(read_only=True)
    collected = serializers.BooleanField(default=False)

    class Meta:
        model = Article
        fields = ("id", "title","content","createtime","user","collected_users","collected","image","visits")
class LabelsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    label_name = serializers.StringRelatedField()
class ArticleSerializerForCreate(serializers.ModelSerializer):
    image = serializers.CharField(required=False, default='',allow_blank=True)

    class Meta:
        model = Article
        exclude = ('collected_users',)
class ArticleSerializerSimple(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ("id", "title")
class UserDetailSerializer(serializers.ModelSerializer):

    articles = ArticleSerializerSimple(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username','avatar','articles','fans')
class CommentSerializerForCreate(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'content','article','user','parent','createtime')
class CommentSerializerItem(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    subs = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model=Comment
        fields = '__all__'
class CommentSerializerList(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    subs = CommentSerializerItem(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = "__all__"

class ArticleSerializerForDetail(serializers.ModelSerializer):
    user = CreateUserSerializer(read_only=True)
    comments = CommentSerializerList(read_only=True, many=True)

    class Meta:
        model = Article
        fields = "__all__"