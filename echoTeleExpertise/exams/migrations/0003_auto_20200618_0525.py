# Generated by Django 3.0.7 on 2020-06-18 04:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0002_request_is_visited'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='notification_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de la notification'),
        ),
        migrations.AlterField(
            model_name='request',
            name='solve_date',
            field=models.DateTimeField(blank=True, verbose_name="Date d'envoi du rapprt"),
        ),
    ]
