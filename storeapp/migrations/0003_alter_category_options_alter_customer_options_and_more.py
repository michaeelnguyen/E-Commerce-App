# Generated by Django 4.0.3 on 2022-04-22 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storeapp', '0002_alter_order_order_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['category_Name'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['customer_Last_Name']},
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['employee_Last_Name']},
        ),
        migrations.AlterModelOptions(
            name='expediter',
            options={'ordering': ['expediter_name']},
        ),
        migrations.AlterModelOptions(
            name='material',
            options={'ordering': ['material_Type']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['product_Name']},
        ),
        migrations.AlterModelOptions(
            name='vendor',
            options={'ordering': ['vendor_name']},
        ),
    ]