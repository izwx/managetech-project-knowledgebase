# Generated by Django 3.2.13 on 2022-12-11 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pyazureboard', '0007_alter_azureboarduser_imageurl'),
    ]

    operations = [
        migrations.RenameField(
            model_name='azureboarduser',
            old_name='imageUrl',
            new_name='avatar',
        ),
    ]