# Generated by Django 2.0.4 on 2019-02-04 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firs_name', models.CharField(blank=True, max_length=256)),
                ('last_name', models.CharField(blank=True, max_length=256)),
                ('company_name', models.CharField(blank=True, max_length=256)),
                ('street_addres_1', models.CharField(blank=True, max_length=256)),
                ('street_addres_2', models.CharField(blank=True, max_length=256)),
                ('city', models.CharField(blank=True, max_length=256)),
                ('city_area', models.CharField(blank=True, max_length=256)),
                ('postal_code', models.CharField(blank=True, max_length=6)),
                ('phonenumber', models.CharField(blank=True, max_length=9)),
            ],
        ),
    ]
