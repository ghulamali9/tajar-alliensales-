# Generated by Django 3.0.7 on 2020-07-01 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20200701_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationsdetails',
            name='discount_amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quotationsdetails',
            name='discount_percentage',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quotationsdetails',
            name='net_amount',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quotationsdetails',
            name='rate',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quotationsdetails',
            name='unit',
            field=models.IntegerField(default=0),
        ),
    ]
