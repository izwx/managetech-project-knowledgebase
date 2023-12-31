# Generated by Django 3.2.13 on 2022-06-17 14:53

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
            name='ChatworkMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.BigIntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('role', models.CharField(db_index=True, max_length=16)),
                ('chatwork_id', models.CharField(db_index=True, max_length=100)),
                ('organization_id', models.IntegerField(blank=True, null=True)),
                ('organization_name', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('avatar_image_url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChatworkRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_id', models.BigIntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(db_index=True, max_length=16)),
                ('icon_path', models.URLField(blank=True, null=True)),
                ('last_update_time', models.IntegerField(blank=True, null=True)),
                ('members', models.ManyToManyField(to='pychatwork.ChatworkMember')),
            ],
        ),
        migrations.CreateModel(
            name='ChatworkTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField(unique=True)),
                ('message_id', models.CharField(max_length=32)),
                ('body', models.TextField(blank=True, null=True)),
                ('limit_time', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(db_index=True, max_length=8)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_account', to='pychatwork.chatworkmember')),
                ('assigned_by_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigend_by_account', to='pychatwork.chatworkmember')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pychatwork.chatworkroom')),
            ],
        ),
        migrations.CreateModel(
            name='ChatworkMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.CharField(max_length=32, unique=True)),
                ('body', models.TextField(blank=True, null=True)),
                ('send_time', models.IntegerField(blank=True, null=True)),
                ('update_time', models.IntegerField(default=0)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pychatwork.chatworkmember')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pychatwork.chatworkroom')),
            ],
        ),
        migrations.CreateModel(
            name='ChatworkFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_id', models.IntegerField(unique=True)),
                ('message_id', models.CharField(max_length=32)),
                ('filesize', models.BigIntegerField(default=0)),
                ('filename', models.FilePathField()),
                ('upload_time', models.IntegerField(blank=True, null=True)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pychatwork.chatworkmember')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pychatwork.chatworkroom')),
            ],
        ),
        migrations.CreateModel(
            name='ChatworkConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_token', models.CharField(max_length=64)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
