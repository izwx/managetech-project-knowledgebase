# Generated by Django 3.2.13 on 2022-06-04 01:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JiraIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('self', models.URLField(unique=True)),
                ('issue_id', models.IntegerField()),
                ('key', models.CharField(max_length=64)),
                ('summary', models.TextField(blank=True, null=True)),
                ('timespent', models.IntegerField(blank=True, null=True)),
                ('expand', models.TextField(blank=True, null=True)),
                ('isWatching', models.BooleanField(default=False)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='JiraIssueType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entityId', models.CharField(max_length=48, unique=True)),
                ('self', models.URLField(unique=True)),
                ('type_id', models.IntegerField()),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True, null=True)),
                ('iconUrl', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JiraPriority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('self', models.URLField(unique=True)),
                ('priority_id', models.IntegerField()),
                ('name', models.CharField(max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='JiraStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('self', models.URLField(unique=True)),
                ('status_id', models.IntegerField()),
                ('name', models.CharField(max_length=24)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JiraUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountId', models.CharField(max_length=32)),
                ('self', models.URLField(unique=True)),
                ('accountType', models.CharField(max_length=24)),
                ('emailAddress', models.EmailField(blank=True, max_length=254, null=True)),
                ('displayName', models.CharField(max_length=64)),
                ('active', models.BooleanField(default=True)),
                ('timeZone', models.CharField(max_length=16)),
                ('locale', models.CharField(max_length=8)),
                ('avatarUrl', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JiraProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=48, unique=True)),
                ('project_id', models.IntegerField()),
                ('key', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True, null=True)),
                ('expand', models.TextField(blank=True, null=True)),
                ('assigneeType', models.CharField(blank=True, max_length=24, null=True)),
                ('projectTypeKey', models.CharField(max_length=16)),
                ('simplified', models.BooleanField(blank=True, null=True)),
                ('style', models.CharField(blank=True, max_length=32, null=True)),
                ('isPrivate', models.BooleanField(blank=True, null=True)),
                ('avatarUrl', models.URLField(blank=True, null=True)),
                ('issues', models.ManyToManyField(to='pyjira.JiraIssue')),
            ],
        ),
        migrations.CreateModel(
            name='JiraIssueComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('self', models.URLField(unique=True)),
                ('comment_id', models.IntegerField()),
                ('body', models.TextField()),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('jsdPublic', models.BooleanField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jira_comment_author', to='pyjira.jirauser')),
                ('updateAuthor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jira_comment_update_author', to='pyjira.jirauser')),
            ],
        ),
        migrations.AddField(
            model_name='jiraissue',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jira_issue_assignee', to='pyjira.jirauser'),
        ),
        migrations.AddField(
            model_name='jiraissue',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jira_issue_creator', to='pyjira.jirauser'),
        ),
        migrations.AddField(
            model_name='jiraissue',
            name='issueType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pyjira.jiraissuetype'),
        ),
        migrations.AddField(
            model_name='jiraissue',
            name='priority',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pyjira.jirapriority'),
        ),
        migrations.AddField(
            model_name='jiraissue',
            name='reporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jira_issue_reporter', to='pyjira.jirauser'),
        ),
        migrations.AddField(
            model_name='jiraissue',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pyjira.jirastatus'),
        ),
        migrations.CreateModel(
            name='JiraConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_url', models.URLField()),
                ('email', models.EmailField(max_length=254)),
                ('api_token', models.CharField(max_length=32)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
