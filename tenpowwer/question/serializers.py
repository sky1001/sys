
from rest_framework import serializers

from article.serialzers import ArticleSerializerForList
from question.models import Question, Reply, Label
from users.models import User
from users.serializers import CreateUserSerializer


class UserSerializerSimple(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')



class ReplySerializerForSubAndParent(serializers.ModelSerializer):

    user = UserSerializerSimple(read_only=True)

    class Meta:
        model = Reply
        fields = ["id", "content","createtime","useful_count","unuseful_count","user"]

class RelySerializers(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

class QueationSerializerForCreate(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    # labels = serializers.StringRelatedField(read_only=True)
    # answer_question = ReplySerializerItem(read_only=True,many=True)
    class Meta:
        model = Question
        fields = '__all__'
class QueationSerializerForList(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    labels = serializers.StringRelatedField(read_only=True)
    # answer_question = ReplySerializerItem(read_only=True,many=True)
    class Meta:
        model = Question
        fields = '__all__'
class ReplySerializerItem(serializers.ModelSerializer):
    subs=ReplySerializerForSubAndParent(read_only=True)
    user= UserSerializerSimple(read_only=True)
    class Meta:
        model = Reply
        fields = '__all__'
class ReplySerializerForList(serializers.ModelSerializer):

    user = UserSerializerSimple(read_only=True)
    subs = ReplySerializerForSubAndParent(read_only=True, many=True)
    parent = ReplySerializerForSubAndParent(read_only=True)

    class Meta:
        model = Reply
        fields = ["id", "content","createtime","useful_count",'problem',"unuseful_count","subs","user","parent"]
class LaderSerializer(serializers.ModelSerializer):
    questions = QueationSerializerForCreate(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    articles = ArticleSerializerForList(read_only=True)
    class Meta:
        model = Label
        fields = '__all__'


class QuestionSerializerForDetail(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    labels = serializers.StringRelatedField(read_only=True, many=True)
    comment_question = ReplySerializerForList(read_only=True, many=True)
    comment_reply = ReplySerializerForList(read_only=True, many=True)
    answer_question = ReplySerializerForList(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ["id","createtime","labels","reply","replyname","replytime","title","unuseful_count","useful_count","user","visits","content","comment_question","comment_reply","answer_question"]

class QuestionSerializerForList(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    labels = serializers.StringRelatedField(read_only=True,many=True)

    class Meta:
        model = Question
        fields = ["id","createtime","labels","reply","replyname","replytime","title","unuseful_count","useful_count","user","visits"]
class LabelSerializerWithQuestionAndArticle(serializers.ModelSerializer):
    questions = QuestionSerializerForList(many=True, read_only=True)
    articles = ArticleSerializerForList(many=True, read_only=True)

    class Meta:
        model = Label
        fields = "__all__"