# Generated by Django 3.2.13 on 2022-06-14 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyslack', '0009_auto_20220614_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slackuser',
            name='color',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
