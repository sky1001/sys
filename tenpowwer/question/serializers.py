from rest_framework import serializers

from question.models import Question


class QueationSerializerForCreate(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Question
        fields = '__all__'
