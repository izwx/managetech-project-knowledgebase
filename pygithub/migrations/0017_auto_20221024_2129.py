# Generated by Django 3.2.13 on 2022-10-24 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pygithub', '0016_githubuser_m_developer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubpullrequest',
            name='assignees',
            field=models.ManyToManyField(blank=True, related_name='github_pr_assignees', to='pygithub.GithubUser'),
        ),
        migrations.AlterField(
            model_name='githubpullrequest',
            name='requested_reviewers',
            field=models.ManyToManyField(blank=True, related_name='github_pr_reviewers', to='pygithub.GithubUser'),
        ),
    ]