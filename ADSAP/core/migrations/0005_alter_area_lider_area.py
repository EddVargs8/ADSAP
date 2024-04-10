# Generated by Django 5.0.3 on 2024-04-10 22:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_permiso_archivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='lider_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mi_empleado', to='core.empleado'),
        ),
    ]
