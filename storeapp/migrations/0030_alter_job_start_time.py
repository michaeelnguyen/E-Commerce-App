# Generated by Django 4.0.3 on 2022-05-09 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0029_remove_job_machine_job_machine_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='start_Time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
