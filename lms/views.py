from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsModer, IsOwner
from .models import Course, Lesson, SubscriptionOnCourse, CoursePayment
from .paginators import CustomPaginator
from .serializers import CourseSerializer, LessonSerializer, CoursePaymentSerializer
from .services import convert_rub_to_dollars, create_stripe_price, create_stripe_session


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPaginator

    def get_queryset(self):
        """Фильтруем набор данных в зависимости от пользователя"""

        if self.request.user.groups.filter(name="Модератор").exists():
            return Course.objects.all()
        user = self.request.user
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """Устанавливает права на действия пользователя."""

        if self.action in (
                "list",
                "retrieve",
                "update",
                "partial_update",
        ):
            permission_classes = [IsAuthenticated, IsModer | IsOwner]
        elif self.action in ("create",):
            permission_classes = [IsAuthenticated, ~IsModer]
        elif self.action in ("destroy",):
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]
    pagination_class = CustomPaginator

    def get_queryset(self):
        """Фильтруем набор данных в зависимости от пользователя"""

        if self.request.user.groups.filter(name="Модератор").exists():
            return Lesson.objects.all()
        user = self.request.user
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]

class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SubscriptionOnCourseAPIView(views.APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')

        course = get_object_or_404(Course, id=course_id)

        # Проверяем, существует ли подписка
        subs_item = SubscriptionOnCourse.objects.filter(user=user, course=course)

        if subs_item.exists():
            # Если подписка существует, удаляем её
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            # Если подписки нет, создаем её
            SubscriptionOnCourse.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)


class CoursePaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = CoursePaymentSerializer
    queryset = CoursePayment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, id=course_id)
        amount_in_dollars = course.price
        # Почему-то не работает конвертация
        # amount_in_dollars = convert_rub_to_dollars(course_price)
        payment = serializer.save(amount=amount_in_dollars)
        price = create_stripe_price(amount_in_dollars, course.name)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
