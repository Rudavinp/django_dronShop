# Generated by Django 2.1.7 on 2019-07-31 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_product_attributes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name'], 'permissions': (('manage_products', 'Manage products'),), 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]