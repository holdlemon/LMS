from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsModer, IsOwner
from .models import Course, Lesson, SubscriptionOnCourse
from .paginators import CustomPaginator
from .serializers import CourseSerializer, LessonSerializer
from .tasks import send_course_update_notification


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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Вызов задачи Celery для отправки уведомлений
        send_course_update_notification.delay(instance.id)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
