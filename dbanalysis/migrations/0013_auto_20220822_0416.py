# Generated by Django 3.2.13 on 2022-08-21 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbanalysis', '0012_remove_dproject_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dteam',
            name='source',
        ),
        migrations.AlterField(
            model_name='dtoolmaster',
            name='tool_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
