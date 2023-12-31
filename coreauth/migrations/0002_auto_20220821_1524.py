# Generated by Django 3.2.13 on 2022-08-21 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coreauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='developer_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Manager'), (2, 'Customer'), (3, 'Project Manager'), (4, 'Developer'), (5, 'Managetech Admin')], null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_status',
            field=models.SmallIntegerField(choices=[(0, 'Provisional'), (1, 'Active'), (-1, 'Stopped')], default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coreauth.dcompany'),
        ),
    ]
