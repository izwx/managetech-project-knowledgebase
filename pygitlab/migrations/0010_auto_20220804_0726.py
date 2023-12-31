# Generated by Django 3.2.13 on 2022-08-04 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pygitlab', '0009_auto_20220717_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gitlabcommit',
            name='short_id',
            field=models.CharField(db_index=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='gitlabproject',
            name='project_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='gitlabuser',
            name='username',
            field=models.CharField(db_index=True, max_length=64),
        ),
        migrations.CreateModel(
            name='GitlabMergeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_id', models.IntegerField(db_index=True)),
                ('request_iid', models.IntegerField(db_index=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=16, null=True)),
                ('merged_at', models.DateTimeField(blank=True, null=True)),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('target_branch', models.CharField(blank=True, db_index=True, max_length=32, null=True)),
                ('source_branch', models.CharField(blank=True, db_index=True, max_length=32, null=True)),
                ('upvotes', models.IntegerField(default=0)),
                ('downvotes', models.IntegerField(default=0)),
                ('web_url', models.URLField(unique=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to='pygitlab.gitlabuser')),
                ('assignees', models.ManyToManyField(blank=True, null=True, related_name='assignees', to='pygitlab.GitlabUser')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to='pygitlab.gitlabuser')),
                ('closed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='closed_by_user', to='pygitlab.gitlabuser')),
                ('merge_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merge_user', to='pygitlab.gitlabuser')),
                ('reviewers', models.ManyToManyField(blank=True, null=True, related_name='reviewers', to='pygitlab.GitlabUser')),
            ],
        ),
    ]
