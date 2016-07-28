# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-28 00:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20160727_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=14),
        ),
    ]