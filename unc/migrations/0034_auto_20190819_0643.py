# Generated by Django 2.2.4 on 2019-08-19 12:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0033_auto_20190817_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 19, 6, 43, 46, 711851), editable=False, null=True),
        ),
    ]
