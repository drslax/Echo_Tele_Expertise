# Generated by Django 3.0.7 on 2020-06-19 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0004_auto_20200619_0334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='is_doctor_visited',
        ),
    ]
