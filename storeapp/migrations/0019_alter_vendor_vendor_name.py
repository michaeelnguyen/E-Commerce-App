# Generated by Django 4.0.3 on 2022-04-06 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0018_alter_expediter_expeditor_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vendor_Name',
            field=models.CharField(choices=[('Dow Chemical', 'Dow Chemical'), ('ExxonMobil', 'ExxonMobil'), ('Adapt Plastics, Inc', 'Adapt Plastics, Inc'), ('A&S Mold & Die Corp', 'A&S Mold & Die Corp')], max_length=30, null=True),
        ),
    ]
