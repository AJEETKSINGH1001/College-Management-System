# Generated by Django 4.2.16 on 2024-12-13 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_alter_courses_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_number', models.CharField(max_length=50, unique=True)),
                ('roll_number', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='student_images/')),
                ('course', models.CharField(max_length=100)),
                ('subjects', models.TextField()),
                ('semester', models.IntegerField()),
                ('batch', models.CharField(max_length=50)),
            ],
        ),
    ]
