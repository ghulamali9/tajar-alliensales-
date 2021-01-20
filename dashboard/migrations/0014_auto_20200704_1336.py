# Generated by Django 3.0.7 on 2020-07-04 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_auto_20200704_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotations',
            name='total_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='quotations',
            name='total_discount_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='quotations',
            name='total_discount_percentage',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='quotationsdetails',
            name='discount_amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='quotationsdetails',
            name='discount_percentage',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='quotationsdetails',
            name='net_amount',
            field=models.FloatField(default=0),
        ),
    ]
