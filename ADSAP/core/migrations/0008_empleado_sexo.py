# Generated by Django 5.0.3 on 2024-04-21 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_noticias_id_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='sexo',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='Masculino', max_length=20),
        ),
    ]