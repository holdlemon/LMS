from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название курса')
    preview = models.ImageField(upload_to='lms/course', blank=True, null=True, verbose_name='Превью курса')
    description = models.TextField(blank=True, null=True, verbose_name='Описание курса')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название урока')
    description = models.TextField(blank=True, null=True, verbose_name='Описание курса')
    preview = models.ImageField(upload_to='lms/lesson', blank=True, null=True, verbose_name='Превью урока')
    url = models.URLField(verbose_name='Ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name='lessons', verbose_name='Курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'