# Generated by Django 2.2.3 on 2019-08-05 17:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0011_auto_20190803_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 5, 11, 32, 50, 359046), editable=False, null=True),
        ),
    ]
