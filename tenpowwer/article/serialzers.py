from rest_framework import serializers
from rest_framework.response import Response

from article.models import Article
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
    # def create(self, validated_data):
    #     # validated_data['user']  = self.view.kwargs
    #     print(validated_data)
    #     admin =super().create(**validated_data)
    #     return admin
class LabelsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    label_name = serializers.StringRelatedField()
class ArticleSerializerForCreate(serializers.ModelSerializer):
    image = serializers.CharField(required=False, default='',allow_blank=True)

    class Meta:
        model = Article
        exclude = ('collected_users',)
