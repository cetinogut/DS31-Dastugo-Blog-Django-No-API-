# Generated by Django 3.2.9 on 2021-12-10 08:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dastugo_blog_app', '0017_alter_post_published_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 12, 10, 8, 34, 9, 151757, tzinfo=utc)),
        ),
    ]
