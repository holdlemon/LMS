from django.apps import apps
from django.contrib import admin

# Получаем все модели текущего приложения
app = apps.get_app_config("users")  # Замените на имя вашего приложения

for model in app.models.values():
    admin.site.register(model)