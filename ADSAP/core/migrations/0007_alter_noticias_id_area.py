# Generated by Django 5.0.3 on 2024-04-16 22:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_estado_solicitud_id_permiso_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticias',
            name='id_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.area'),
        ),
    ]
