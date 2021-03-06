# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-31 11:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rencontre', '0002_auto_20160328_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='search_children',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='search_gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='F', max_length=1),
        ),
        migrations.AddField(
            model_name='profile',
            name='search_religion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='search_status',
            field=models.CharField(choices=[('D', 'Divorced'), ('S', 'Single'), ('O', 'Others')], default='S', max_length=1),
        ),
    ]
