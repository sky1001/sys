from django.db import models

from datetime import datetime

# 吐槽和吐槽的评论数据都存储在mongodb中,不是存储在mysql中
# 吐槽和吐槽的评论都属于吐槽的这张表
# 吐槽的parent_id为None,评论则有parent_id
class Spit(models.Model):
    content = models.TextField(max_length=10000, verbose_name="吐槽内容") # 吐槽内容
    publishtime = models.DateTimeField(default=datetime.utcnow) # 发布日期
    userid = models.CharField(max_length=100, verbose_name="发布人ID") # 发布人ID
    nickname = models.CharField(max_length=100, verbose_name="发布人昵称") # 发布人昵称
    visits = models.IntegerField(default=0, verbose_name="浏览量") # 浏览量
    thumbup = models.IntegerField(default=0, verbose_name="点赞数") # 点赞数
    comment = models.IntegerField(default=0, verbose_name="回复数") # 回复数
    avatar = models.CharField(max_length=100, verbose_name="用户的头像") # 用户的头像
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, related_name='subs', null=True, blank=True, verbose_name="被吐槽的吐槽") # 上级ID
    collected = models.BooleanField(default=False) # 是否收藏
    hasthumbup = models.BooleanField(default=False) # 是否点赞

    class Meta:
        db_table = "tb_spit"
        verbose_name = "吐槽"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content
