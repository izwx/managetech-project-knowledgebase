# Generated by Django 3.2.13 on 2022-09-29 17:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pygitlab', '0014_alter_gitlabwiki_encoding'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitlabwiki',
            name='reg_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
