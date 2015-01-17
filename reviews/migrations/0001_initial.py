# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('score', models.PositiveSmallIntegerField(help_text=b'Integer score in a range from 1 through 5', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('comment', models.TextField(help_text=b'A comment explaining the score for the review', max_length=1000, blank=True)),
                ('anonymous', models.BooleanField(default=False, help_text=b'Keep the reviewer identity anonymous')),
                ('comment_approved', models.BooleanField(default=True, help_text=b'The comment has been approved by an admin')),
                ('created', models.DateTimeField(help_text=b'Date and time created', auto_now_add=True)),
                ('modified', models.DateTimeField(help_text=b'Date and time last modified', auto_now=True)),
                ('content_type', models.ForeignKey(help_text=b'Reviewed model', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='reviews', to=settings.AUTH_USER_MODEL, help_text=b'User that submitted the review')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
