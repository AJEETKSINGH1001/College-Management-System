# Generated by Django 4.2.16 on 2024-12-17 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_remove_marks_student_name_marks_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='marks',
            name='courses',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.courses'),
        ),
    ]