# Generated by Django 3.0.7 on 2020-07-23 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_auto_20200722_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='customer_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Customers'),
        ),
    ]
