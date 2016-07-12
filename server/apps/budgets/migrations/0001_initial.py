# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-12 05:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254)),
                ('budget_type', models.CharField(choices=[('expense', 'Expense'), ('savings', 'Savings'), ('debt', 'Debt')], max_length=254)),
                ('goal', models.DecimalField(decimal_places=2, max_digits=14)),
                ('goal_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=14)),
                ('period', models.CharField(blank=True, choices=[('yearly', 'Yearly'), ('monthly', 'Monthly'), ('weekly', 'Weekly'), ('daily', 'Daily')], max_length=254, null=True)),
                ('payment_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='accounts.AppUser')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('description', models.CharField(blank=True, max_length=254, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=14)),
                ('transaction_type', models.CharField(choices=[('debit', 'Debit'), ('credit', 'Credit')], max_length=254)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.Account')),
                ('budget', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='budgets.Budget')),
                ('tags', models.ManyToManyField(blank=True, to='budgets.Tag')),
            ],
        ),
    ]
