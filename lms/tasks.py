from celery import shared_task
from django.core.mail import send_mail

from config.settings import DEFAULT_FROM_EMAIL
from lms.models import Course


@shared_task
def send_course_update_notification(course_id):
    """Асинхронная задача для отправки уведомлений об обновлении курса."""
    course = Course.objects.get(id=course_id)
    subscriptions = course.course_subscription.all()
    recipient_emails = [subscription.user.email for subscription in subscriptions]

    subject = f'Обновление курса: {course.name}'
    message = f'Курс "{course.name}" был обновлен. Проверьте новые материалы!'
    from_email = DEFAULT_FROM_EMAIL

    send_mail(subject, message, from_email, recipient_emails)