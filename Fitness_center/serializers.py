from rest_framework import serializers
from Fitness_center.models import Client, Subscription, TrainingType
from django.contrib.auth.models import User

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'password', 'phone']

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['user_id', 'subscription_purchase_date', 'subscription_end_date', 'status', 'gender', 'training_type', 'subscription_period']

class TrainingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingType
        fields = ['name', 'description', 'price']
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def validate_email(self, value):
        # Кастомна валідація для формату електронної пошти
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError('Електронна пошта повинна закінчуватися на @gmail.com.')
        return value

    def validate_password(self, value):
        # Кастомна валідація для паролю (наприклад, довжина паролю)
        if len(value) < 8:
            raise serializers.ValidationError('Пароль повинен бути не менше 8 символів.')
        return value

    def validate(self, data):
        # Перевірка, чи користувач з таким ім'ям вже існує
        username = data.get('email')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Користувач з таким іменем вже існує.')
        return data

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        user = User.objects.create_user(**validated_data)
        return user