# Generated by Django 2.2.4 on 2019-08-15 14:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0024_merge_20190815_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 15, 8, 45, 16, 713569), editable=False, null=True),
        ),
    ]
