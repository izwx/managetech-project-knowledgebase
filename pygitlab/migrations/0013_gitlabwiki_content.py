# Generated by Django 3.2.13 on 2022-09-20 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pygitlab', '0012_auto_20220804_1135'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitlabwiki',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
