# Generated by Django 4.2.16 on 2024-12-17 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_marks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marks',
            name='student_name',
        ),
        migrations.AddField(
            model_name='marks',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.studentdetails'),
        ),
    ]