# Generated by Django 3.2.13 on 2022-05-29 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pygithub', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GithubCommit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sha', models.CharField(max_length=64, unique=True)),
                ('html_url', models.URLField(unique=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('verified', models.BooleanField()),
                ('verification_reason', models.CharField(max_length=16)),
                ('verification_signature', models.CharField(blank=True, max_length=100, null=True)),
                ('verification_payload', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GithubUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(unique=True)),
                ('login', models.CharField(max_length=64, unique=True)),
                ('node_id', models.CharField(max_length=32, unique=True)),
                ('avatar_url', models.URLField(unique=True)),
                ('html_url', models.URLField(unique=True)),
                ('type', models.CharField(max_length=16)),
                ('site_admin', models.BooleanField()),
                ('name', models.CharField(max_length=64)),
                ('company', models.CharField(max_length=64)),
                ('blog', models.URLField()),
                ('location', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='GithubRepository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('full_name', models.CharField(max_length=255, unique=True)),
                ('owner', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('html_url', models.URLField(unique=True)),
                ('default_branch', models.CharField(max_length=32)),
                ('open_issues', models.IntegerField(default=0)),
                ('open_issues_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField()),
                ('assignees', models.ManyToManyField(related_name='github_assignees', to='pygithub.GithubUser')),
                ('collaborators', models.ManyToManyField(related_name='github_collaborators', to='pygithub.GithubUser')),
            ],
        ),
        migrations.CreateModel(
            name='GithubCommitComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_id', models.IntegerField(unique=True)),
                ('html_url', models.URLField(unique=True)),
                ('body', models.TextField()),
                ('path', models.URLField()),
                ('position', models.IntegerField()),
                ('line', models.IntegerField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('commit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pygithub.githubcommit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pygithub.githubuser')),
            ],
        ),
        migrations.AddField(
            model_name='githubcommit',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='github_commit_author', to='pygithub.githubuser'),
        ),
        migrations.AddField(
            model_name='githubcommit',
            name='committer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='github_committer', to='pygithub.githubuser'),
        ),
    ]
