# Generated by Django 3.2.13 on 2022-10-19 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pygitlab', '0017_gitlabmergerequest_m_project_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='gitlabuser',
            name='m_developer_id',
            field=models.BigIntegerField(blank=True, db_index=True, null=True),
        ),
    ]
