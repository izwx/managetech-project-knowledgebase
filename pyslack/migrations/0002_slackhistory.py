# Generated by Django 3.2.13 on 2022-06-14 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pyslack', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SlackHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=32)),
                ('subtype', models.CharField(max_length=32)),
                ('ts', models.FloatField()),
                ('text', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pyslack.slackuser')),
            ],
        ),
    ]
