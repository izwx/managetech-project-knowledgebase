# Generated by Django 3.2.13 on 2022-10-03 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pygithub', '0014_githubpullrequest_requested_reviewers'),
    ]

    operations = [
        migrations.AddField(
            model_name='githubpullrequest',
            name='m_project_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
