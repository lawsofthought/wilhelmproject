# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-01 07:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presenter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='liveexperimentsession',
            name='city',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='liveexperimentsession',
            name='country_code',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='liveexperimentsession',
            name='country_code_alt',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='liveexperimentsession',
            name='country_name',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='liveexperimentsession',
            name='ip_address',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='liveexperimentsession',
            name='ua_browser',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='liveexperimentsession',
            name='ua_browser_version',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='liveexperimentsession',
            name='ua_device',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='liveexperimentsession',
            name='ua_os',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='liveexperimentsession',
            name='ua_os_version',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='liveexperimentsession',
            name='ua_string',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='liveexperimentsession',
            name='ua_string_pp',
            field=models.TextField(null=True),
        ),
    ]