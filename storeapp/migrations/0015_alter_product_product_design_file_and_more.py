# Generated by Django 4.0.3 on 2022-04-06 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0014_alter_product_product_design_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_Design_File',
            field=models.FileField(null=True, upload_to='media/storeapp/product_files'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_Image',
            field=models.ImageField(null=True, upload_to='media/storeapp/product_images'),
        ),
    ]
