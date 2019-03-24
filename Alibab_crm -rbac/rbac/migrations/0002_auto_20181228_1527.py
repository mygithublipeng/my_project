# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-28 07:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(max_length=64, verbose_name='URL别名'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='url',
            field=models.CharField(max_length=108, verbose_name='权限'),
        ),
    ]
