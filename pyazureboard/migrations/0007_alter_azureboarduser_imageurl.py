# Generated by Django 3.2.13 on 2022-12-11 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyazureboard', '0006_azureboarduser_imageurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='azureboarduser',
            name='imageUrl',
            field=models.TextField(blank=True, null=True),
        ),
    ]
