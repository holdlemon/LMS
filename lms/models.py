from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название курса')
    preview = models.ImageField(upload_to='lms/course', blank=True, null=True, verbose_name='Превью курса')
    description = models.TextField(blank=True, null=True, verbose_name='Описание курса')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    price = models.PositiveIntegerField(default=1000, verbose_name='Цена')

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
    price = models.PositiveIntegerField(default=1000, verbose_name='Цена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class SubscriptionOnCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_subscription', verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_subscription', verbose_name='Курс')

    def __str__(self):
        return f"{self.user.name} подписан на {self.course.name}"

    class Meta:
        verbose_name = 'Подписка на курс'
        verbose_name_plural = 'Подписки на курсы'


# class CoursePayment(models.Model):
#     amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
#     session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID сессии')
#     link = models.URLField(max_length=400, blank=True, null=True, verbose_name='Ссылка на оплату')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, blank=True, null=True, verbose_name='Пользователь')
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
#
#     def __str__(self):
#         return self.amount
#
#     class Meta:
#         verbose_name = 'Оплата курса'
#         verbose_name_plural = 'Оплаты курсов'