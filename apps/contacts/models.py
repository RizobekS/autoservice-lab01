from django.db import models


class ContactMessage(models.Model):
    name = models.CharField('Имя', max_length=256)
    email = models.EmailField('Email')
    text = models.TextField('Сообщение')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f'Сообщение от {self.name} ({self.created_at:%d.%m.%Y %H:%M})' if self.created_at else f'Сообщение от {self.name}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Сообщение из контактов'
        verbose_name_plural = 'Сообщения из контактов'
