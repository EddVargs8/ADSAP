# Generated by Django 5.0.3 on 2024-05-05 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_merge_20240504_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='fecha_ingreso',
            field=models.DateField(auto_now_add=True),
        ),
    ]
