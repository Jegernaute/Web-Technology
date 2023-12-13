from django.test import TestCase
from .serializers import ClientSerializer
from .models import Client
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .serializers import UserRegistrationSerializer
from rest_framework import status
from django.urls import reverse


class ClientSerializerTest(TestCase):
    def setUp(self):
        self.client_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'password': 'securepassword',
            'phone': '1234567890'
        }
        self.serializer = ClientSerializer(data=self.client_data)

    def test_valid_data(self):
        self.assertTrue(self.serializer.is_valid())

    def test_invalid_data(self):
        invalid_data = {
            'first_name': 'Jane',
            'email': 'invalidemail'  # Invalid email format
        }
        serializer = ClientSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_save(self):
        serializer = ClientSerializer(data=self.client_data)
        serializer.is_valid()
        instance = serializer.save()
        self.assertIsInstance(instance, Client)

class UserRegistrationSerializerTest(APITestCase):
    def test_valid_data(self):
        # Правильні дані користувача
        data = {
            'email': 'example@gmail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        # Невірний формат електронної пошти
        data = {
            'email': 'example@example.com',  # Невірний формат
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Електронна пошта повинна закінчуватися на @gmail.com.', serializer.errors['email'])

    def test_invalid_password(self):
        # Невірний пароль (занадто короткий)
        data = {
            'email': 'example@gmail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'pass'  # Пароль занадто короткий
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('Пароль повинен бути не менше 8 символів.', serializer.errors['password'])

    def test_existing_user(self):
        # Створення користувача з такою електронною поштою
        existing_user = User.objects.create_user(username='existinguser', email='existing@gmail.com', password='password')
        # Дані для нового користувача
        data = {
            'email': 'existing@gmail.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123'
        }
        # Серіалайзуємо дані нового користувача
        serializer = UserRegistrationSerializer(data=data)
        # Перевірка валідації
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertIn('Користувач з такою електронною поштою вже існує.', serializer.errors['email'])

class ClientListViewTest(APITestCase):
    def test_get_clients(self):
        url = reverse('client-list')  # Перевірте, чи це ім'я шляху для вашого списку клієнтів
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

