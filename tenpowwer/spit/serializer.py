from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from spit.models import Spit

class SpitSerializer(serializers.ModelSerializer):
    userid = serializers.CharField(max_length=100,required=False)
    nickname = serializers.CharField(max_length=100,required=False)
    avatar = serializers.CharField(max_length=100,required=False)
    class Meta:
        model = Spit
        fields = "__all__"
    def create(self, validated_data):
        spit = super().create(validated_data)
        try:
            user = self.context['request'].user
        except:
            user = None
        # 判断是否是吐槽别人的吐槽
        if spit.parent:
            # 判断是否登陆
            if user and user.is_authenticated:
                spit.userid = str(user.id)
                spit.nickname = user.nickname if user.nickname else user.username
                spit.avatar = user.avatar
                spit.save()
                spit.parent.comment += 1
                spit.parent.save()
                return spit
            else:
                raise ValidationError('未登录')
        else:
            return spit



