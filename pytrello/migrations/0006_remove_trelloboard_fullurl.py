# Generated by Django 3.2.13 on 2022-09-20 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pytrello', '0005_auto_20220920_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trelloboard',
            name='fullUrl',
        ),
    ]
