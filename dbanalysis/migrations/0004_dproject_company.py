# Generated by Django 3.2.13 on 2022-07-10 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbanalysis', '0003_dcompany'),
    ]

    operations = [
        migrations.AddField(
            model_name='dproject',
            name='company',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dbanalysis.dcompany'),
            preserve_default=False,
        ),
    ]
