# Generated by Django 4.2.2 on 2023-06-14 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tguser',
            old_name='char_id',
            new_name='chat_id',
        ),
    ]
