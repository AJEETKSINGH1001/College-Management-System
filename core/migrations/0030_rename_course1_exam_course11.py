# Generated by Django 4.2.16 on 2024-12-13 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_alter_exam_subjects'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='course1',
            new_name='course11',
        ),
    ]
