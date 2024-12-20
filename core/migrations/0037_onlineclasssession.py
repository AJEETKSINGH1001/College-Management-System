# Generated by Django 4.2.16 on 2024-12-20 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_results_courses_results_exam_alter_marks_exam'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineClassSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('meeting_link', models.URLField(blank=True, null=True)),
                ('meeting_id', models.CharField(blank=True, max_length=100, null=True)),
                ('meeting_password', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.batch')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_sessions', to='core.studentdetails')),
            ],
        ),
    ]