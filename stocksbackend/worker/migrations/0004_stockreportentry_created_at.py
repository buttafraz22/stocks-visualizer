# Generated by Django 5.0.4 on 2024-06-25 07:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0003_alter_symbolinformation_symbol_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockreportentry',
            name='created_at',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
