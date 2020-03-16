from rest_framework import serializers
from article.models import Article
class ChannelsSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.StringRelatedField()

class ArticleSerializerForList(serializers.ModelSerializer):
    # user = UserDetailSerializer(read_only=True)
    collected = serializers.BooleanField(default=False)

    class Meta:
        model = Article
        fields = ("id", "title","content","createtime","user","collected_users","collected","image","visits")
class LabelsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    label_name = serializers.StringRelatedField()