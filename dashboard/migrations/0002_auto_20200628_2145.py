# Generated by Django 3.0.7 on 2020-06-28 16:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='designation',
            name='created_on',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='designation',
            name='deleted_on',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='designation',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='designation',
            name='is_updated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='designation',
            name='updated_on',
            field=models.DateField(null=True),
        ),
    ]
