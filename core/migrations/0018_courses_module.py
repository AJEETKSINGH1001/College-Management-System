# Generated by Django 4.2.16 on 2024-12-09 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_performance_delete_performanceevaluation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField(blank=True)),
                ('credit_hours', models.IntegerField()),
                ('duration_weeks', models.IntegerField()),
                ('department', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField(blank=True)),
                ('hours', models.IntegerField()),
                ('courses', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='core.courses')),
            ],
        ),
    ]