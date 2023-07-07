# Generated by Django 3.2.13 on 2022-11-14 00:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pyazureboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='azureboardworkitem',
            name='assignedTo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='azureboard_workitem_assign', to='pyazureboard.azureboarduser'),
        ),
    ]