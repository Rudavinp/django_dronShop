# Generated by Django 2.1.7 on 2020-01-28 08:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0012_auto_20200127_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 28, 8, 10, 38, 181409, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sale',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 28, 8, 10, 38, 182341, tzinfo=utc)),
        ),
    ]
