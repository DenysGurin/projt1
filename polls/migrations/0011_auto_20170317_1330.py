# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-17 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20170316_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='image',
            field=models.FileField(null=True, upload_to='polls/static'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='picture',
            field=models.CharField(default='', help_text='input filename.format', max_length=60),
        ),
    ]
