# Generated by Django 3.2.13 on 2022-09-20 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pygitlab', '0013_gitlabwiki_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gitlabwiki',
            name='encoding',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
