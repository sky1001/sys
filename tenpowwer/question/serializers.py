from rest_framework import serializers

from question.models import Question, Reply
from users.serializers import CreateUserSerializer


class RelySerializers(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

class QueationSerializerForCreate(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    labels = serializers.StringRelatedField(read_only=True)
    # answer_question = ReplySerializerItem(read_only=True,many=True)
    class Meta:
        model = Question
        fields = '__all__'
class ReplySerializerItem(serializers.ModelSerializer):
    subs=RelySerializers(read_only=True)
    user= CreateUserSerializer(read_only=True)
    class Meta:
        model = Reply
        fields = '__all__'

class QuestionSerializerForDetail(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    labels = serializers.StringRelatedField(read_only=True, many=True)
    # replies = ReplySerializerForList(read_only=True, many=True)
    comment_question = ReplySerializerItem(read_only=True, many=True)
    comment_reply = ReplySerializerItem(read_only=True, many=True)
    answer_question = ReplySerializerItem(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ["id","createtime","labels","reply","replyname","replytime","title","unuseful_count","useful_count","user","visits","content","comment_question","comment_reply","answer_question"]