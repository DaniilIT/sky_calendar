from django.db import models

from core.models import User


class TgUser(models.Model):
    chat_id = models.BigIntegerField('Chat_ID', unique=True)
    username = models.CharField('Username', max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None,
                             verbose_name='Пользователь', related_name='tg')
    verification_code = models.CharField('Код доступа', max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = 'Телеграмм'
        verbose_name_plural = 'Телеграммы'

    def __str__(self):
        return self.username
