# Generated by Django 4.2.16 on 2024-12-19 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.IntegerField()),
                ('batch', models.CharField(max_length=50)),
                ('total_marks_obtained', models.FloatField()),
                ('total_max_marks', models.FloatField()),
                ('gpa', models.FloatField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course1')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.studentdetails')),
            ],
        ),
        migrations.DeleteModel(
            name='Result',
        ),
    ]