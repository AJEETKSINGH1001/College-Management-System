# Generated by Django 4.2.16 on 2024-12-04 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='some_field',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
