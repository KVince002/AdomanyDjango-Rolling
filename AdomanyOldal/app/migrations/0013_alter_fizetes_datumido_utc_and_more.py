# Generated by Django 4.0.4 on 2022-07-07 17:03

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0012_alter_fizetes_datumido_utc_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fizetes',
            name='datumIdo_UTC',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 7, 17, 3, 34, 990449, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='gyujtes',
            name='datumIdo_UTC',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 7, 17, 3, 34, 989610, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='visszautalas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mennyit', models.IntegerField()),
                ('datumIdo_UTC', models.DateTimeField(default=datetime.datetime(2022, 7, 7, 17, 3, 34, 991215, tzinfo=utc))),
                ('ki', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
