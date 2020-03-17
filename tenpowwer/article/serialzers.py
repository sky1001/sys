from rest_framework import serializers
from rest_framework.response import Response

from article.models import Article, Comment
from users.serializers import CreateUserSerializer

class CommentSerializerItem(serializers.ModelSerializer):
    user = CreateUserSerializer(read_only=True)
    subs = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model=Comment
        fields = '__all__'
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
class CommentSerializer(serializers.ModelDurationField):
    user = serializers.StringRelatedField(read_only=True)
    subs = CommentSerializerItem(read_only=True, many=True)
    class Meta:
        model = Comment
        fields = '__all__'
class ArticleSerializerForDetail(serializers.ModelSerializer):
    user = CreateUserSerializer(read_only=True)
    comments = CommentSerializerItem(read_only=True, many=True)

    class Meta:
        model = Article
        fields = "__all__"