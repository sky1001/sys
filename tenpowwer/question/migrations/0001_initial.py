# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.CharField(default=None, max_length=20, null=True, verbose_name='标签名称')),
                ('desc', models.CharField(default=None, max_length=200, null=True, verbose_name='标签描述')),
                ('baike_url', models.CharField(default=None, max_length=200, null=True, verbose_name='标签百科链接')),
                ('label_icon', models.ImageField(default=None, null=True, upload_to='', verbose_name='标签图 片')),
                ('users', models.ManyToManyField(related_name='labels', to=settings.AUTH_USER_MODEL, verbose_name='关注者')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
                'db_table': 'tb_label',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=100, null=True, verbose_name='标题')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(default='', verbose_name='问题内容')),
                ('visits', models.BigIntegerField(default=0, null=True, verbose_name='浏览量')),
                ('thumbup', models.BigIntegerField(default=0, null=True, verbose_name='点赞数')),
                ('reply', models.BigIntegerField(default=0, null=True, verbose_name='回复数')),
                ('useful_count', models.BigIntegerField(default=0, null=True, verbose_name='有 用数')),
                ('unuseful_count', models.BigIntegerField(default=0, null=True, verbose_name='无用数')),
                ('solve', models.CharField(default=None, max_length=1, null=True, verbose_name='是否解决')),
                ('createtime', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建日期')),
                ('updatetime', models.DateTimeField(auto_now=True, null=True, verbose_name='修 改日期')),
                ('replyname', models.CharField(default=None, max_length=100, null=True, verbose_name='回复人昵称')),
                ('replytime', models.DateTimeField(default=None, null=True, verbose_name='回复日 期')),
                ('labels', models.ManyToManyField(related_name='questions', to='question.Label')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to=settings.AUTH_USER_MODEL, verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '问题',
                'verbose_name_plural': '问题',
                'db_table': 'tb_question',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(default='', verbose_name='回答内容')),
                ('createtime', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建日期')),
                ('updatetime', models.DateTimeField(auto_now=True, null=True, verbose_name='修 改日期')),
                ('useful_count', models.BigIntegerField(default=0, null=True, verbose_name='有用 数')),
                ('unuseful_count', models.BigIntegerField(default=0, null=True, verbose_name='无用数')),
                ('type', models.IntegerField(default=0, verbose_name='回答类型')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subs', to='question.Reply', verbose_name='父评论')),
                ('problem', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='question.Question', verbose_name='问题ID')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to=settings.AUTH_USER_MODEL, verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '回答',
                'verbose_name_plural': '回答',
                'db_table': 'qa_reply',
                'ordering': ['-createtime'],
            },
        ),
    ]
