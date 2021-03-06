# Generated by Django 2.2.2 on 2019-07-19 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FARM_API', '0005_auto_20190719_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='waterneedrecommenderinfo',
            name='setpoint_value',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3),
        ),
        migrations.AddField(
            model_name='waterneedrecommenderinfo',
            name='use_sys_setpoint',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='waterneedrecommenderinfo',
            name='zone',
            field=models.CharField(default='', max_length=30),
        ),
    ]
