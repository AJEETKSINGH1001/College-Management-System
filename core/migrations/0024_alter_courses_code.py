# Generated by Django 4.2.16 on 2024-12-10 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_rename_course_batch_courses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='code',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]