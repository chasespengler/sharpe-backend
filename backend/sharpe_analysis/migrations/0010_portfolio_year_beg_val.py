# Generated by Django 2.2.7 on 2022-08-26 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharpe_analysis', '0009_auto_20220826_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='year_beg_val',
            field=models.FloatField(default=0),
        ),
    ]