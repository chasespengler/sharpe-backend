# Generated by Django 2.2.7 on 2022-08-09 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stat_micro', '0002_auto_20220809_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='securitystats',
            name='mean',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='securitystats',
            name='sd',
            field=models.FloatField(null=True),
        ),
    ]