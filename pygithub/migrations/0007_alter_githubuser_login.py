# Generated by Django 3.2.13 on 2022-05-29 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pygithub', '0006_alter_githubuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubuser',
            name='login',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
