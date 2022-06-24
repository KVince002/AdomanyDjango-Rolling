# Generated by Django 4.0.4 on 2022-06-24 11:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_fizetes_ido_alter_gyujtes_ido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='felhasznalo',
            name='telefon',
        ),
        migrations.AlterField(
            model_name='fizetes',
            name='datum',
            field=models.DateField(default=datetime.date(2022, 6, 24)),
        ),
        migrations.AlterField(
            model_name='fizetes',
            name='ido',
            field=models.TimeField(default=datetime.time(11, 0, 5, 587445)),
        ),
        migrations.AlterField(
            model_name='gyujtes',
            name='datum',
            field=models.DateField(default=datetime.date(2022, 6, 24)),
        ),
        migrations.AlterField(
            model_name='gyujtes',
            name='ido',
            field=models.TimeField(default=datetime.time(11, 0, 5, 586656)),
        ),
    ]