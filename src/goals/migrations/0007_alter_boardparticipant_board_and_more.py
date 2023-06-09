# Generated by Django 4.2.2 on 2023-06-13 14:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0006_alter_goalcategory_board_alter_goalcategory_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boardparticipant',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='participants', to='goals.board', verbose_name='Доска'),
        ),
        migrations.AlterField(
            model_name='boardparticipant',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='participants', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
