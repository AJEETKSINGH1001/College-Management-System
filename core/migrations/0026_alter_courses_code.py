# Generated by Django 4.2.16 on 2024-12-10 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_batch_courses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='code',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
