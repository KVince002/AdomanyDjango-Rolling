# Generated by Django 4.0.4 on 2022-06-24 12:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_gyujtes_datumido_utc_alter_fizetes_datumido_utc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fizetes',
            name='datumIdo_UTC',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 24, 12, 21, 31, 857015, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='gyujtes',
            name='datumIdo_UTC',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 24, 12, 21, 31, 856248, tzinfo=utc)),
        ),
    ]
