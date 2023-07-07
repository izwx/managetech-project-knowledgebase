# Generated by Django 3.2.13 on 2022-09-18 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbanalysis', '0017_alter_dprojecttoolinfo_payload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dprojecttoolinfo',
            name='tool_id',
            field=models.IntegerField(choices=[(1, 'jira'), (2, 'slack'), (3, 'chatwork'), (4, 'github'), (5, 'gitlab'), (6, 'trello'), (7, 'redmine')]),
        ),
    ]
