# Generated by Django 3.2.9 on 2021-12-09 08:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dastugo_blog_app', '0011_auto_20211209_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 12, 9, 8, 0, 19, 885680, tzinfo=utc)),
        ),
    ]