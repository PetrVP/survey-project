# Generated by Django 3.0.3 on 2021-04-22 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey_api', '0004_useranswer_got_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useranswer',
            name='got_answer',
        ),
    ]