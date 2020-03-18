# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gathering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100, null=True, verbose_name='活动名称')),
                ('summary', models.TextField(default=None, null=True, verbose_name='活动简介')),
                ('detail', ckeditor_uploader.fields.RichTextUploadingField(default='', verbose_name='详细介绍')),
                ('address', models.CharField(default=None, max_length=100, null=True, verbose_name='举办地点')),
                ('sponsor', models.CharField(default=None, max_length=100, null=True, verbose_name='主办方')),
                ('image', models.ImageField(default=None, null=True, upload_to='', verbose_name='活动图片')),
                ('city', models.CharField(default=None, max_length=100, null=True, verbose_name='举办城市')),
                ('state', models.SmallIntegerField(choices=[(0, '不可见'), (1, '可见')], default=1, verbose_name='是否可见')),
                ('starttime', models.DateTimeField(null=True, verbose_name='开始时间')),
                ('endtime', models.DateTimeField(null=True, verbose_name='截止日期')),
                ('endrolltime', models.DateTimeField(null=True, verbose_name='报名截止日期')),
            ],
            options={
                'verbose_name': '活动',
                'verbose_name_plural': '活动',
                'db_table': 'tb_gathering',
            },
        ),
    ]
