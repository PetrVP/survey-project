# Generated by Django 3.0.3 on 2021-04-22 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey_api', '0002_survey_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='user',
            field=models.CharField(max_length=20, verbose_name='Пользователь'),
        ),
    ]
