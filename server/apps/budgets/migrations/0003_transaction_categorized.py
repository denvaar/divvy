# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-04-08 17:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0002_transaction_ignore'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='categorized',
            field=models.BooleanField(default=False),
        ),
    ]