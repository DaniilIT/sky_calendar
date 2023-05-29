from django.db import models

from core.models import User


class BaseModel(models.Model):
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    updated = models.DateTimeField('Дата последнего обновления', auto_now=True)

    class Meta:
        abstract = True

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         self.created = timezone.now()
    #     self.updated = timezone.now()
    #     return super().save(*args, **kwargs)


class GoalCategory(BaseModel):
    title = models.CharField('Название', max_length=255)
    is_deleted = models.BooleanField('Удалена', default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Автор')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title
