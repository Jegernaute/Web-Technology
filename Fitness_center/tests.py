from django.test import TestCase
from .serializers import ClientSerializer, SubscriptionSerializer, TrainingTypeSerializer
from .models import Client, TrainingType, Subscription
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .serializers import UserRegistrationSerializer
from rest_framework import status
from django.urls import reverse, resolve
from Fitness_center.views import (
    ClientList,
    ClientDetail,
    TrainingTypeList,
    TrainingTypeDetail,
    SubscriptionList,
    SubscriptionDetail,
    register_user,
)
from django.test import SimpleTestCase
from rest_framework.urls import views as drf_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


#_____________test_serializers_____________
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

class SubscriptionSerializerTest(TestCase):
    def setUp(self):
        self.training_type = TrainingType.objects.create(
            name='Хатха-йога',
            description='Sample description',
            price=50.0
        )
        self.client = Client.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            password='password',
            phone='1234567890'
        )
        self.subscription = Subscription.objects.create(
            user_id=self.client,
            subscription_purchase_date='2023-12-31',
            subscription_end_date='2024-12-31',
            status='Активна',
            gender='Чоловіча',
            training_type=self.training_type,
            subscription_period=30
        )

    def test_status_validation(self):
        data = {
            'user_id': self.subscription.user_id.id,
            'subscription_purchase_date': '2023-12-31',
            'subscription_end_date': '2024-12-31',
            'status': 'Активна',
            'gender': 'Чоловіча',
            'training_type': self.training_type.id,
            'subscription_period': 30
        }
        serializer = SubscriptionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['status'], 'Активна')

    def test_invalid_data(self):
        data = {
            'user_id': self.client.id,
            'subscription_purchase_date': '2021-12-31',
            'subscription_end_date': '2024-12-31',
            'status': 'Абоба',
            'gender': 'Чоловіча',
            'training_type': self.training_type.id,
            'subscription_period': 30
        }
        serializer = SubscriptionSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_serializer_save(self):
        new_subscription_data = {
            'user_id': self.client.id,
            'subscription_purchase_date': '2023-12-31',
            'subscription_end_date': '2024-12-31',
            'status': 'Активна',
            'gender': 'Чоловіча',
            'training_type': self.training_type.id,
            'subscription_period': 30
        }
        serializer = SubscriptionSerializer(data=new_subscription_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        # Перевірка, чи дані було успішно збережено
        saved_subscriptions = Subscription.objects.filter(user_id=self.client)
        self.assertTrue(saved_subscriptions.exists())
class TrainingTypeSerializerTest(TestCase):
    def test_training_type_serialization(self):
        # Правильні дані
        valid_training_data = {
            'name': 'Хатха-йога',
            'description': 'Sample description',
            'price': 50.0
        }
        serializer = TrainingTypeSerializer(data=valid_training_data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data
        self.assertEqual(serialized_data['name'], 'Хатха-йога')
        self.assertEqual(serialized_data['description'], 'Sample description')
        self.assertEqual(float(serialized_data['price']), 50.0)

    def test_invalid_training_type_data(self):
        # Тест на недійсні дані
        invalid_training_data = {
            'name': '',  # Пусте значення для імені
            'description': 'Sample description',
            'price': -50.0  # Негативна ціна
        }
        invalid_serializer = TrainingTypeSerializer(data=invalid_training_data)
        self.assertFalse(invalid_serializer.is_valid())  # Перевірка на недійсність даних

    def test_serializer_save(self):
        # Тест збереження серіалізатора
        valid_training_data_to_save = {
            'name': 'Хатха-йога',
            'description': 'Sample description',
            'price': 50.0
        }
        serializer_to_save = TrainingTypeSerializer(data=valid_training_data_to_save)
        self.assertTrue(serializer_to_save.is_valid())
        serializer_to_save.save()  # Збереження
        # Перевірка, чи дані було успішно збережено
        saved_training_type = TrainingType.objects.get(name='Хатха-йога')  # Отримання об'єкта з бази даних
        self.assertEqual(saved_training_type.description, 'Sample description')
        self.assertEqual(float(saved_training_type.price), 50.0)
class UserRegistrationSerializerTest(APITestCase):
    def setUp(self):
        self.valid_data = {
            'email': 'user@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123'
        }

    def test_registration_with_invalid_email(self):
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'test'
        response = self.client.post('/api/manager/register/', data=invalid_data)
        self.assertEqual(response.status_code, 400)

        # Перевірка наявності 'email' у відповіді
        self.assertIn('email', response.json())

        # Перевірка тексту помилки, використовуючи 'in'
        expected_error = 'Enter a valid email address.'
        actual_error = response.json()['email'][0]
        self.assertIn(expected_error, actual_error)

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

#_____________test_views_____________
class ClientListViewTest(APITestCase):
    def test_get_clients(self):
        url = reverse('client-list')  # Перевірте, чи це ім'я шляху для вашого списку клієнтів
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#_____________test_urls_____________
class TestUrls(SimpleTestCase):

    def test_client_list_url_resolves(self):
        url = reverse('client-list')
        self.assertEqual(resolve(url).func.view_class, ClientList)

    def test_client_detail_url_resolves(self):
        url = reverse('client-detail', args=[1])  # assuming pk=1 for testing purposes
        self.assertEqual(resolve(url).func.view_class, ClientDetail)

    def test_training_type_list_url_resolves(self):
        url = reverse('trainingtype-list')
        self.assertEqual(resolve(url).func.view_class, TrainingTypeList)

    def test_training_type_detail_url_resolves(self):
        url = reverse('trainingtype-detail', args=[1])  # assuming pk=1 for testing purposes
        self.assertEqual(resolve(url).func.view_class, TrainingTypeDetail)

    def test_subscription_list_url_resolves(self):
        url = reverse('subscription-list')
        self.assertEqual(resolve(url).func.view_class, SubscriptionList)

    def test_subscription_detail_url_resolves(self):
        url = reverse('subscription-detail', args=[1])  # assuming pk=1 for testing purposes
        self.assertEqual(resolve(url).func.view_class, SubscriptionDetail)

    def test_register_user_url_resolves(self):
        url = reverse('register_user')
        self.assertEqual(resolve(url).func, register_user)

    def test_token_obtain_pair_url_resolves(self):
        url = reverse('token_obtain_pair')
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)

    def test_token_refresh_url_resolves(self):
        url = reverse('token_refresh')
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

    def test_drf_auth_url_resolves(self):
        url = reverse('drf-auth:login')
        self.assertEqual(resolve(url).func.view_class, drf_views.LoginView)

