# Generated by Django 3.2.13 on 2022-09-20 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pytrello', '0008_trellocard_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='trellocard',
            name='due',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
