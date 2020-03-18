# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Spit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=10000, verbose_name='吐槽内容')),
                ('publishtime', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('userid', models.CharField(max_length=100, verbose_name='发布人ID')),
                ('nickname', models.CharField(max_length=100, verbose_name='发布人昵称')),
                ('visits', models.IntegerField(default=0, verbose_name='浏览量')),
                ('thumbup', models.IntegerField(default=0, verbose_name='点赞数')),
                ('comment', models.IntegerField(default=0, verbose_name='回复数')),
                ('avatar', models.CharField(max_length=100, verbose_name='用户的头像')),
                ('collected', models.BooleanField(default=False)),
                ('hasthumbup', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subs', to='spit.Spit', verbose_name='被吐槽的吐槽')),
            ],
            options={
                'verbose_name': '吐槽',
                'verbose_name_plural': '吐槽',
                'db_table': 'tb_spit',
            },
        ),
    ]
