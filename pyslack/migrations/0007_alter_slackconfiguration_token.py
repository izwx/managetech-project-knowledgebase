# Generated by Django 3.2.13 on 2022-06-14 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyslack', '0006_auto_20220614_0820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slackconfiguration',
            name='token',
            field=models.CharField(max_length=100),
        ),
    ]
