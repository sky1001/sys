from rest_framework import serializers
class ArticleSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.StringRelatedField()
