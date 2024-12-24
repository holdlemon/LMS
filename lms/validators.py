from rest_framework.exceptions import ValidationError


def validate_youtube_url(value):
    """ Проверяет, что ссылка содержит 'youtube.com'."""

    if 'youtube.com' not in value:
        raise ValidationError("Ссылки на сторонние ресурсы, кроме youtube.com, запрещены.")
