# Generated by Django 3.2.13 on 2022-07-17 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pygithub', '0010_rename_configuartion_mygithubrepository_configuration'),
    ]

    operations = [
        migrations.CreateModel(
            name='GithubPullRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pull_request_id', models.IntegerField(unique=True)),
                ('html_url', models.URLField(unique=True)),
                ('issue_url', models.URLField(blank=True, null=True)),
                ('diff_url', models.URLField(blank=True, null=True)),
                ('number', models.IntegerField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=16, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField()),
                ('closed_at', models.DateTimeField()),
                ('merged_at', models.DateTimeField()),
                ('merge_commit_sha', models.CharField(db_index=True, max_length=100)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='github_pr_assignee', to='pygithub.githubuser')),
                ('assignees', models.ManyToManyField(related_name='github_pr_assignees', to='pygithub.GithubUser')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='github_pr_user', to='pygithub.githubuser')),
            ],
        ),
    ]
