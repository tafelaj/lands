# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-21 21:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lrms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landsuser',
            name='local_authority',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='lrms.Authority'),
        ),
    ]
