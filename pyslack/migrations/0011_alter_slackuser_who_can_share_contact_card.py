# Generated by Django 3.2.13 on 2022-06-14 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyslack', '0010_alter_slackuser_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slackuser',
            name='who_can_share_contact_card',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
