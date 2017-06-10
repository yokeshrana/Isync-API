# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-27 14:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_notes_nno'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='username',
            field=models.TextField(default=django.utils.timezone.now, max_length=15),
            preserve_default=False,
        ),
    ]