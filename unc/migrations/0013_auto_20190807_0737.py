# Generated by Django 2.2.3 on 2019-08-07 13:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0012_auto_20190805_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='due',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 7, 7, 37, 34, 545308), editable=False, null=True),
        ),
    ]
