# Generated by Django 4.0.3 on 2022-05-09 02:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0026_remove_machine_job_job_machine_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='machine_ID',
            new_name='machine',
        ),
    ]