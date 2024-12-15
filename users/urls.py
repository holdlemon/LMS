from rest_framework.routers import SimpleRouter

from .apps import UsersConfig
from .views import PaymentViewSet, UserViewSet

app_name = UsersConfig.name

router_user = SimpleRouter()
router_user.register(r"user", UserViewSet)

router_payment = SimpleRouter()
router_payment.register(r"payment", PaymentViewSet)

urlpatterns = router_user.urls + router_payment.urls
