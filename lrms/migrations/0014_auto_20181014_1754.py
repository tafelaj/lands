# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-10-14 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lrms', '0013_auto_20181014_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_number',
            field=models.CharField(choices=[('RNT', 'Payment for Land Rentals'), ('NO', 'New Occupancy'), ('OLR', 'Old Land Record'), ('PF', 'Penalty Fees')], default='elysian', max_length=5),
        ),
    ]
