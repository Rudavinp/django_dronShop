# Generated by Django 2.1.7 on 2020-01-27 13:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0011_auto_20200127_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 27, 13, 49, 8, 100870, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sale',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 27, 13, 49, 8, 101821, tzinfo=utc)),
        ),
    ]
