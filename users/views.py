from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from lms.models import Course, Lesson
from users.models import User, Payment
from users.permissions import IsUser
from users.serializers import UserSerializer, PaymentSerializer, UserCommonSerializer, PaymentCreateSerializer
from users.services import create_stripe_price, create_stripe_session, create_stripe_product


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
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "method"]
    ordering_fields = [
        "payment_date",
    ]

    def get_serializer_class(self):
        # Используем PaymentCreateSerializer для POST-запросов
        if self.request.method == 'POST':
            return PaymentCreateSerializer
        # Используем PaymentSerializer для других запросов
        return PaymentSerializer

    def perform_create(self, serializer):
        # Сохраняем платеж
        payment = serializer.save(user=self.request.user)

        # Получаем объект курса или урока из сохраненного платежа
        product = payment.lesson or payment.course
        if not product:
            raise ValueError("Не указан ни курс, ни урок.")

        # Получаем название и цену продукта
        item_name = product.name
        item = create_stripe_product(item_name)
        amount = product.price

        # Логика для Stripe
        try:
            price = create_stripe_price(item, amount)
            session_id, payment_link = create_stripe_session(price)
        except Exception as e:
            # Логируем ошибку, если что-то пошло не так
            print(f"Ошибка при создании сессии Stripe: {e}")
            raise ValidationError({"error": "Ошибка при создании платежа в Stripe."})

        # Обновляем платеж
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


# class PaymentCreateAPIView(generics.CreateAPIView):
#     serializer_class = PaymentSerializer
#     queryset = Payment.objects.all()
#
#     def perform_create(self, serializer):
#         # Сохраняем платеж
#         payment = serializer.save(user=self.request.user)
#         # Получаем данные из запроса
#         course_id = self.request.data.get('course')
#         lesson_id = self.request.data.get('lesson')
#
#         # Получаем объект курса или урока
#         if course_id:
#             item = get_object_or_404(Course, id=course_id)
#             item_name = item.name
#             amount_in_dollars = item.price
#         else:
#             item = get_object_or_404(Lesson, id=lesson_id)
#             item_name = item.name
#             amount_in_dollars = item.price
#
#         # Логика для Stripe
#         payment = serializer.save(amount=amount_in_dollars)
#         price = create_stripe_price(amount_in_dollars, item_name)
#         session_id, payment_link = create_stripe_session(price)
#
#         # Обновляем платеж
#         payment.session_id = session_id
#         payment.link = payment_link
#         payment.save()
