# Generated by Django 2.2.4 on 2019-08-20 21:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0038_auto_20190820_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 20, 15, 21, 31, 987095), editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='domain',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
