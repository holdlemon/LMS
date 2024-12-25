from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apps import UsersConfig
from .views import PaymentViewSet, UserViewSet, PaymentCreateAPIView

app_name = UsersConfig.name

router_user = SimpleRouter()
router_user.register(r"user", UserViewSet)

router_payment = SimpleRouter()
router_payment.register(r"payment", PaymentViewSet)

urlpatterns = router_user.urls + router_payment.urls + [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("payment/", PaymentCreateAPIView.as_view(), name="payment")
]
