# Generated by Django 4.0.3 on 2022-04-21 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_Status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered')], max_length=255, null=True),
        ),
    ]
