# Generated by Django 2.2.3 on 2019-08-03 14:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0010_auto_20190803_0614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 3, 8, 59, 50, 858935), editable=False, null=True),
        ),
    ]
