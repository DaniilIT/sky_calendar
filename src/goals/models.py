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
                             verbose_name='Автор', related_name='categories')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Goal(BaseModel):
    class Status(models.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(models.IntegerChoices):
        low = 1, 'Низкий'
        medium = 2, 'Средний'
        high = 3, 'Высокий'
        critical = 4, 'Критический'

    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)
    due_date = models.DateTimeField('Дата выполнения', null=True, blank=True)
    status = models.PositiveSmallIntegerField('Статус', choices=Status.choices,
                                              default=Status.to_do)
    priority = models.PositiveSmallIntegerField('Приоритет', choices=Priority.choices,
                                                default=Priority.medium)

    category = models.ForeignKey(GoalCategory, on_delete=models.SET_NULL, null=True,
                                 verbose_name='Категория', related_name='goals')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Автор', related_name='goals')

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    def __str__(self):
        return self.title


class GoalComment(BaseModel):
    text = models.TextField('Текст')

    goal = models.ForeignKey(Goal, on_delete=models.CASCADE,
                             verbose_name='Цель', related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Автор', related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
