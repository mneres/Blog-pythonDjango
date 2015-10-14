# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('url', models.CharField(default='', max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('tag', models.CharField(default='', max_length=50, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='post',
            name='published_date',
        ),
        migrations.AddField(
            model_name='post',
            name='url',
            field=models.CharField(default='', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(default='', max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='', max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='tag',
            name='post',
            field=models.ForeignKey(to='blog.Post', related_name='tags'),
        ),
        migrations.AddField(
            model_name='image',
            name='post',
            field=models.ForeignKey(to='blog.Post', related_name='images'),
        ),
    ]
