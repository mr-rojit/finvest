# Generated by Django 5.0.1 on 2024-02-09 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_remove_dailydata_adjusted_close'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
