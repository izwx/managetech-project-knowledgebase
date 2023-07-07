# Generated by Django 3.2.13 on 2022-07-03 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbanalysis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DDomainMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DSkillMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DSkillDeveloper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('months', models.IntegerField(default=1)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.ddeveloper')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dskillmaster')),
            ],
        ),
        migrations.CreateModel(
            name='DDomainDeveloper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('months', models.IntegerField(default=1)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.ddeveloper')),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.ddomainmaster')),
            ],
        ),
        migrations.CreateModel(
            name='DDocumentDeveloperSprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_documents', models.IntegerField(default=0)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.ddeveloper')),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dsprint')),
            ],
        ),
    ]