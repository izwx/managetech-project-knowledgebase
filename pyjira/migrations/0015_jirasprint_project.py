# Generated by Django 3.2.13 on 2022-10-12 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pyjira', '0014_jiraproject_m_project_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='jirasprint',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pyjira.jiraproject'),
        ),
    ]
