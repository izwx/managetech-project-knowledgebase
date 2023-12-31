# Generated by Django 3.2.13 on 2022-09-25 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyredmine', '0007_redmineversion'),
    ]

    operations = [
        migrations.AddField(
            model_name='redmineversion',
            name='estimated_hours',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='redmineversion',
            name='spent_hours',
            field=models.FloatField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='redmineversion',
            unique_together={('domain_url', 'version_id')},
        ),
    ]
