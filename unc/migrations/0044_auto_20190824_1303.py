# Generated by Django 2.2.4 on 2019-08-24 19:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0043_auto_20190824_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 24, 13, 3, 8, 745783), editable=False, null=True),
        ),
    ]
