# Generated by Django 2.1.7 on 2020-01-29 05:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0015_auto_20200129_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='sale',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
