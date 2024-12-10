from django.core.management import call_command
from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = "Добавление данных из фикстур"

    def handle(self, *args, **kwargs):

        # Удаляем существующие записи
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        User.objects.all().delete()
        Payment.objects.all().delete()

        # создание фикстур - команды для терминала
        # python -Xutf8 manage.py dumpdata lms.Course --output course_fixture.json --indent 4
        # python -Xutf8 manage.py dumpdata lms.Lesson --output lesson_fixture.json --indent 4
        # python -Xutf8 manage.py dumpdata users.User --output user_fixture.json --indent 4
        # python -Xutf8 manage.py dumpdata users.Payment --output payment_fixture.json --indent 4

        # Добавляем данные из фикстур
        call_command("loaddata", "course_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Курсы загружены из фикстур успешно"))
        call_command("loaddata", "lesson_fixture.json", format="json")
        self.stdout.write(self.style.SUCCESS("Уроки загружены из фикстур успешно"))

        # создаем тестовых пользователей их платежи
        # Пользователь №1
        user = User.objects.create(
            email="test1@test1.ru",
        )
        user.set_password("123qwe456rty")
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создан тестовый пользователь с email {user.email} с паролем 123qwe456rty "
            )
        )

        payment = Payment.objects.create(
            user=user,
            course=Course.objects.get(id=1),
            amount=999.99,
        )
        payment.save()

        payment = Payment.objects.create(
            user=user,
            lesson=Lesson.objects.get(id=1),
            amount=99.99,
        )
        payment.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно добавлены платежи для пользователя с email {user.email}"
            )
        )

        # Пользователь №2
        user = User.objects.create(
            email="test2@test2.ru",
        )
        user.set_password("123qwe456rty")
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создан тестовый пользователь с email {user.email} с паролем 123qwe456rty "
            )
        )

        payment = Payment.objects.create(
            user=user,
            course=Course.objects.get(id=2),
            amount=999.99,
        )
        payment.save()

        payment = Payment.objects.create(
            user=user,
            lesson=Lesson.objects.get(id=2),
            amount=99.99,
        )
        payment.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно добавлены платежи для пользователя с email {user.email}"
            )
        )
