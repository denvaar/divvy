# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-11 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='fi',
            field=models.CharField(default='erase', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='userid',
            field=models.CharField(default='erase', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='account',
            name='userpass',
            field=models.CharField(default='erase', max_length=254),
            preserve_default=False,
        ),
    ]