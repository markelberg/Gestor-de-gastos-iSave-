# Generated by Django 5.0.4 on 2024-04-18 08:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mi_gestor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gasto',
            name='fecha',
            field=models.DateField(default=datetime.date.today),
        ),
    ]