from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .apps import UsersConfig
from .views import PaymentViewSet, UserViewSet

app_name = UsersConfig.name

root_router = DefaultRouter()
root_router.register(r'users', UserViewSet, 'users')
root_router.register(r'payments', PaymentViewSet, 'payments')

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += root_router.urls
