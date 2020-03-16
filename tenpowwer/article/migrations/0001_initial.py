# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2020-03-15 12:42
from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=100, null=True, verbose_name='标题')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(default='', verbose_name='文章内容')),
                ('image', models.CharField(default=None, max_length=100, null=True, verbose_name='文章封面')),
                ('createtime', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建日期')),
                ('updatetime', models.DateTimeField(auto_now=True, null=True, verbose_name='修改日期')),
                ('visits', models.IntegerField(default=0, null=True, verbose_name='浏览量')),
                ('thumbup', models.IntegerField(default=0, null=True, verbose_name='点赞数')),
                ('comment_count', models.IntegerField(default=0, null=True, verbose_name='评论数')),
            ],
            options={
                'verbose_name': '文章',
                'verbose_name_plural': '文章',
                'db_table': 'tb_article',
                'ordering': ['-createtime'],
            },
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100, null=True, verbose_name='频道名称')),
            ],
            options={
                'verbose_name': '频道',
                'verbose_name_plural': '频道',
                'db_table': 'tb_channel',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(default='', max_length=1000, verbose_name='回答内容')),
                ('createtime', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建日期')),
                ('updatetime', models.DateTimeField(auto_now=True, null=True, verbose_name='修改日期')),
                ('article', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='article.Article', verbose_name='问题ID')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subs', to='article.Comment', verbose_name='父评论')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
                'db_table': 'article_comment',
                'ordering': ['-createtime'],
            },
        ),
    ]
