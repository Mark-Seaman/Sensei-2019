# Generated by Django 2.2.4 on 2019-10-22 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unc', '0054_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='due',
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]
