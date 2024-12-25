from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

    def validate(self, data):
        # Получаем значения курса и урока
        course = data.get('course')
        lesson = data.get('lesson')

        # Проверяем, что указан либо курс, либо урок, но не оба одновременно
        if course and lesson:
            raise serializers.ValidationError("Укажите либо курс, либо урок, но не оба одновременно.")
        if not course and not lesson:
            raise serializers.ValidationError("Необходимо указать либо курс, либо урок.")

        return data


class UserSerializer(serializers.ModelSerializer):

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Хешируем пароль с использованием set_password
        user = User(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Хешируем пароль при обновлении, если пароль предоставлен
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class UserCommonSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "email")
