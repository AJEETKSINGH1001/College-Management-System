# Generated by Django 4.2.16 on 2024-12-07 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_performanceevaluation_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='avg_rating',
            field=models.FloatField(default=0.0),
        ),
    ]
