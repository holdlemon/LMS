from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User, Payment
from users.permissions import IsUser
from users.serializers import UserSerializer, PaymentSerializer, UserCommonSerializer


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
