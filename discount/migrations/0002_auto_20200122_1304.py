# Generated by Django 2.1.7 on 2020-01-22 13:04

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 22, 13, 4, 32, 291628, tzinfo=utc)),
        ),
    ]
