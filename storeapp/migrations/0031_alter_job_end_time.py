# Generated by Django 4.0.3 on 2022-05-09 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0030_alter_job_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='end_Time',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]