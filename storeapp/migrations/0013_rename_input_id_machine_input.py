# Generated by Django 4.0.3 on 2022-04-22 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0012_remove_job_machine_id_machine_job'),
    ]

    operations = [
        migrations.RenameField(
            model_name='machine',
            old_name='input_ID',
            new_name='input',
        ),
    ]
