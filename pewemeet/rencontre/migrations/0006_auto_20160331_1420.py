# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-31 11:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rencontre', '0005_profile_search_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='search_country',
            field=models.ForeignKey(default='IL', on_delete=django.db.models.deletion.CASCADE, related_name='search_country', to='cities_light.Country'),
        ),
    ]
