# Generated by Django 2.2.4 on 2019-11-27 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insight', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insight',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
