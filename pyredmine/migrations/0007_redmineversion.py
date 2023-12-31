# Generated by Django 3.2.13 on 2022-09-25 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pyredmine', '0006_alter_redminewiki_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedmineVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_url', models.URLField()),
                ('version_id', models.BigIntegerField()),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(db_index=True, max_length=16)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('sharing', models.CharField(blank=True, max_length=32, null=True)),
                ('wiki_page_title', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField()),
                ('updated_on', models.DateTimeField()),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pyredmine.redmineproject')),
            ],
            options={
                'unique_together': {('domain_url', 'project', 'version_id')},
            },
        ),
    ]
