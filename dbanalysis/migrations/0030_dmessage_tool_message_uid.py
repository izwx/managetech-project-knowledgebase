# Generated by Django 3.2.13 on 2023-02-05 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbanalysis', '0029_dchannel_dmention_dmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='dmessage',
            name='tool_message_uid',
            field=models.BigIntegerField(db_index=True, default=None),
            preserve_default=False,
        ),
    ]
