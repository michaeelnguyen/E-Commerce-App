# Generated by Django 4.0.3 on 2022-04-06 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0011_alter_product_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_Image',
            field=models.ImageField(upload_to=''),
        ),
    ]
