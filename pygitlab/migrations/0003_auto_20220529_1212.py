# Generated by Django 3.2.13 on 2022-05-29 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pygitlab', '0002_alter_gitlabbranch_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gitlabuser',
            name='expires_at',
        ),
        migrations.RemoveField(
            model_name='gitlabuser',
            name='membership_state',
        ),
    ]