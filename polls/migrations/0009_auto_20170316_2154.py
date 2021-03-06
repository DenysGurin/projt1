# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-16 21:54
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20170316_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='image',
            field=models.FileField(null=True, storage=django.core.files.storage.FileSystemStorage(location='/polls/media'), upload_to=''),
        ),
        migrations.AlterField(
            model_name='poll',
            name='picture',
            field=models.CharField(help_text='input filename.type', max_length=60),
        ),
    ]
