# Generated by Django 3.0.7 on 2020-06-20 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0003_auto_20200620_0711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('M', 'Homme'), ('F', 'Femme')], max_length=1, verbose_name='Sexe'),
        ),
    ]
