# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-11 19:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('bartlett', '0004_playlist_misc'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaylistV2',
            fields=[
                ('uid', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('instructions', jsonfield.fields.JSONField(null=True)),
                ('max_slides', models.IntegerField(blank=True, default=3, null=True)),
                ('misc', jsonfield.fields.JSONField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SessionPlaylistV2',
            fields=[
                ('uid', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('initialized', models.BooleanField(default=False)),
                ('datetime_initialized', models.DateTimeField(null=True)),
                ('started', models.BooleanField(default=False)),
                ('datetime_started', models.DateTimeField(null=True)),
                ('completed', models.BooleanField(default=False)),
                ('datetime_completed', models.DateTimeField(null=True)),
                ('current_slide_rank', models.PositiveIntegerField(null=True)),
                ('playlist_uid', models.CharField(max_length=40, null=True)),
                ('playlist_ct', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bartlett_sessionplaylistv2_as_playlist', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]