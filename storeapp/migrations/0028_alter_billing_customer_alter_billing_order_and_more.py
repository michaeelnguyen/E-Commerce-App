# Generated by Django 4.0.3 on 2022-05-09 04:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0027_rename_machine_id_job_machine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='storeapp.customer'),
        ),
        migrations.AlterField(
            model_name='billing',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='storeapp.order'),
        ),
        migrations.AlterField(
            model_name='inputitem',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='storeapp.vendor'),
        ),
        migrations.AlterField(
            model_name='job',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='storeapp.employee'),
        ),
        migrations.AlterField(
            model_name='job',
            name='machine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='storeapp.machine'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='storeapp.order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='storeapp.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='job_ID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='storeapp.job'),
        ),
        migrations.AlterField(
            model_name='product',
            name='material_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='storeapp.material'),
        ),
        migrations.AlterField(
            model_name='product',
            name='version_ID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='versionList', to='storeapp.version'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='storeapp.customer'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='expediter_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='storeapp.expediter'),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='storeapp.order'),
        ),
        migrations.AlterField(
            model_name='version',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='storeapp.customer'),
        ),
    ]