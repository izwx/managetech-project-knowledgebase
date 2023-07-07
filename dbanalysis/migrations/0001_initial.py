# Generated by Django 3.2.13 on 2022-07-03 05:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DDeveloper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, choices=[('github', 'GITHUB'), ('gitlab', 'GITLAB'), ('slack', 'SLACK'), ('chatwork', 'CHATWORK'), ('jira', 'JIRA'), ('trello', 'TRELLO'), ('redmine', 'REDMINE')], max_length=10, null=True)),
                ('developer_name', models.CharField(max_length=100)),
                ('avg_velocity', models.FloatField(default=0)),
                ('avg_work_rate', models.FloatField(default=0)),
                ('num_documents', models.IntegerField(default=0)),
                ('avg_lead_time', models.FloatField(default=0)),
                ('avg_reviews', models.IntegerField(default=0)),
                ('avg_review_hours', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, choices=[('github', 'GITHUB'), ('gitlab', 'GITLAB'), ('slack', 'SLACK'), ('chatwork', 'CHATWORK'), ('jira', 'JIRA'), ('trello', 'TRELLO'), ('redmine', 'REDMINE')], max_length=10, null=True)),
                ('group_name', models.CharField(max_length=100)),
                ('parent_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dgroup')),
            ],
        ),
        migrations.CreateModel(
            name='DProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, choices=[('github', 'GITHUB'), ('gitlab', 'GITLAB'), ('slack', 'SLACK'), ('chatwork', 'CHATWORK'), ('jira', 'JIRA'), ('trello', 'TRELLO'), ('redmine', 'REDMINE')], max_length=10, null=True)),
                ('project_name', models.CharField(max_length=100)),
                ('sprint_week', models.IntegerField(default=1)),
                ('total_num_members', models.IntegerField(default=1)),
                ('avg_velocity', models.FloatField(default=0)),
                ('avg_work_rate', models.FloatField(default=0)),
                ('num_of_documents', models.IntegerField(default=0)),
                ('current_sprint_id', models.CharField(max_length=64)),
                ('progress_rate', models.FloatField(default=0)),
                ('avg_lead_time', models.FloatField(default=0)),
                ('remain_work_hour', models.FloatField(default=0)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('expect_release_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DSprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sprint_name', models.CharField(max_length=100)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('num_ticket', models.IntegerField(default=0)),
                ('total_work_hour', models.IntegerField(default=0)),
                ('work_hour_persion', models.IntegerField(default=0)),
                ('close_work_hour', models.IntegerField(default=0)),
                ('velocity', models.FloatField(default=0)),
                ('avg_work_rate', models.FloatField(default=0)),
                ('num_new_tickets', models.IntegerField(default=0)),
                ('num_pull_request', models.IntegerField(default=0)),
                ('num_prs_merged', models.IntegerField(default=0)),
                ('num_message', models.IntegerField(default=0)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dproject')),
            ],
        ),
        migrations.CreateModel(
            name='DToolMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tool_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('difficulty', models.PositiveSmallIntegerField(default=1)),
                ('start_date', models.DateTimeField()),
                ('expect_hours', models.IntegerField(default=0)),
                ('work_hours', models.IntegerField(default=0)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('lead_time', models.FloatField(blank=True, null=True)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.ddeveloper')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dproject')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dsprint')),
            ],
        ),
        migrations.CreateModel(
            name='DTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(blank=True, choices=[('github', 'GITHUB'), ('gitlab', 'GITLAB'), ('slack', 'SLACK'), ('chatwork', 'CHATWORK'), ('jira', 'JIRA'), ('trello', 'TRELLO'), ('redmine', 'REDMINE')], max_length=10, null=True)),
                ('team_name', models.CharField(max_length=100)),
                ('avg_velocity', models.FloatField(default=0)),
                ('avg_work_rate', models.FloatField(default=0)),
                ('num_of_documents', models.IntegerField(default=0)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dgroup')),
            ],
        ),
        migrations.CreateModel(
            name='DPullRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('work_hours', models.IntegerField(default=0)),
                ('num_reviews', models.IntegerField(default=0)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.ddeveloper')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dproject')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dsprint')),
            ],
        ),
        migrations.CreateModel(
            name='DProjectTeamMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dproject')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dteam')),
            ],
        ),
        migrations.CreateModel(
            name='DDeveloperTool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(max_length=100)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.ddeveloper')),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dtoolmaster')),
            ],
        ),
        migrations.CreateModel(
            name='DDeveloperTeamMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_hour', models.IntegerField(default=40)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.ddeveloper')),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dteam')),
            ],
        ),
        migrations.CreateModel(
            name='DDeveloperProjectSprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('velocity', models.FloatField(default=10)),
                ('total_expected_work_hours', models.IntegerField(default=10)),
                ('num_documents', models.IntegerField(default=0)),
                ('num_messages', models.IntegerField(default=0)),
                ('avg_lead_time', models.FloatField(default=0)),
                ('num_new_ticket', models.IntegerField(default=0)),
                ('num_pull_requests', models.IntegerField(default=0)),
                ('num_prs_merged', models.IntegerField(default=0)),
                ('num_reviews', models.IntegerField(default=0)),
                ('review_hours', models.IntegerField(default=0)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.ddeveloper')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dproject')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dsprint')),
            ],
        ),
    ]
