from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import SET_NULL

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта', help_text='Укажите почту')
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name='Телефон', help_text='Укажите телефон')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Город', help_text='Укажите город')
    avatar = models.ImageField(upload_to='users/avatars', blank=True, null=True, verbose_name='Аватар', help_text='Загрузите аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    CASH = 'cash'
    TRANSFER = 'transfer'

    METHOD_CHOICES = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, blank=True, null=True, verbose_name='Пользователь')
    payment_date = models.DateField(auto_now_add=True, verbose_name='Дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name='payments_for_course', verbose_name='Курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True, related_name='payments_for_lesson', verbose_name='Урок')
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    method = models.CharField(choices=METHOD_CHOICES, default=CASH ,verbose_name='Способ оплаты')
    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID сессии')
    link = models.URLField(max_length=400, blank=True, null=True, verbose_name='Ссылка на оплату')

    def __str__(self):
        return f"Платеж {self.amount} от {self.user}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
