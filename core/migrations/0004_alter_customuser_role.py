# Generated by Django 4.2.16 on 2024-12-04 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_customuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('parent', 'Parent')], default='student', max_length=20),
        ),
    ]
