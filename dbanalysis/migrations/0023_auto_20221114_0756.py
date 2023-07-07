# Generated by Django 3.2.13 on 2022-11-13 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbanalysis', '0022_auto_20221105_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ddevelopertoolmap',
            name='tool_id',
            field=models.IntegerField(choices=[(1, 'jira'), (2, 'slack'), (3, 'chatwork'), (4, 'github'), (5, 'gitlab'), (6, 'trello'), (7, 'redmine'), (8, 'backlog'), (9, 'confluence'), (10, 'azure')]),
        ),
        migrations.AlterField(
            model_name='dprojecttoolinfo',
            name='tool_id',
            field=models.IntegerField(choices=[(1, 'jira'), (2, 'slack'), (3, 'chatwork'), (4, 'github'), (5, 'gitlab'), (6, 'trello'), (7, 'redmine'), (8, 'backlog'), (9, 'confluence'), (10, 'azure')]),
        ),
    ]