# Generated by Django 3.0.7 on 2020-07-05 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_auto_20200704_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationsdetails',
            name='quatation_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Quotations'),
        ),
    ]
