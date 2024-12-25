from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from lms.models import Course, Lesson
from users.models import User, Payment
from users.permissions import IsUser
from users.serializers import UserSerializer, PaymentSerializer, UserCommonSerializer
from users.services import create_stripe_price, create_stripe_session


class UserViewSet(viewsets.ModelViewSet):

    model = User
    queryset = User.objects.all()

    def get_serializer_class(self):
        if (
                self.action in ("retrieve", "update", "partial_update", "destroy")
                and self.request.user.email == self.get_object().email
        ):
            return UserSerializer
        return UserCommonSerializer

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            permission_classes = [IsAuthenticated, IsUser]
        elif self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]


class PaymentViewSet(viewsets.ModelViewSet):

    model = Payment
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "method"]
    ordering_fields = [
        "payment_date",
    ]

class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        # Сохраняем платеж
        payment = serializer.save(user=self.request.user)
        # Получаем данные из запроса
        course_id = self.request.data.get('course')
        lesson_id = self.request.data.get('lesson')

        # Получаем объект курса или урока
        if course_id:
            item = get_object_or_404(Course, id=course_id)
            item_name = item.name
            amount_in_dollars = item.price
        else:
            item = get_object_or_404(Lesson, id=lesson_id)
            item_name = item.name
            amount_in_dollars = item.price

        # Логика для Stripe
        payment = serializer.save(amount=amount_in_dollars)
        price = create_stripe_price(amount_in_dollars, item_name)
        session_id, payment_link = create_stripe_session(price)

        # Обновляем платеж
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()
