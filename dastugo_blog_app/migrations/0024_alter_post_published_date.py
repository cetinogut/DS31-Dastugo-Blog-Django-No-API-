# Generated by Django 3.2.9 on 2021-12-11 00:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dastugo_blog_app', '0023_alter_post_published_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 12, 11, 0, 4, 49, 87980, tzinfo=utc)),
        ),
    ]