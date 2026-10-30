from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Tour, Category, BookingRequest, Card, UserTour
from .forms import CustomUserCreationForm, BookingRequestForm, CardForm

User = get_user_model()


class ModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Пляжный отдых", slug="beach")
        self.tour = Tour.objects.create(
            title="Мальдивы",
            category=self.category,
            description="Отдых мечты",
            price=120000.00,
            duration=7
        )

    def test_tour_creation(self):
        """Проверка создания тура и его строкового представления"""
        self.assertEqual(self.tour.title, "Мальдивы")
        self.assertEqual(str(self.tour), "Мальдивы")
        self.assertEqual(self.tour.category.name, "Пляжный отдых")

    def test_user_creation(self):
        """Проверка создания пользователя"""
        user = User.objects.create_user(username="testuser", password="testpassword123", phone="+79991234567")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpassword123"))
        self.assertEqual(user.phone, "+79991234567")


class FormTests(TestCase):
    def test_user_creation_form_valid(self):
        """Тест валидной формы регистрации"""
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'phone': '+79991112233',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
            'pd_consent': True,
            'terms': True
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_creation_form_invalid_password(self):
        """Тест невалидной формы: пароли не совпадают"""
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'phone': '+79991112233',
            'password1': 'StrongPassword123',
            'password2': 'DifferentPassword123',
            'pd_consent': True,
            'terms': True
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_booking_form_valid(self):
        """Тест формы обратной связи"""
        form_data = {
            'name': 'Иван',
            'email': 'ivan@example.com',
            'phone': '+79998887766',
            'message': 'Хочу тур в Египет',
            'privacy': True
        }
        form = BookingRequestForm(data=form_data)
        self.assertTrue(form.is_valid())


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Горы", slug="mountains")
        self.tour = Tour.objects.create(
            title="Эльбрус", category=self.category, description="Восхождение", price=50000, duration=5
        )
        self.user = User.objects.create_user(username="testuser", password="testpassword123")

    def test_home_view(self):
        """Тест главной страницы (должна возвращать 200)"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')
        self.assertContains(response, "Эльбрус")

    def test_tour_list_view_and_search(self):
        """Тест списка туров и поиска"""
        response = self.client.get(reverse('tour_list'))
        self.assertEqual(response.status_code, 200)

        # Тест поиска
        response_search = self.client.get(reverse('tour_list') + '?q=Эльбрус')
        self.assertContains(response_search, "Эльбрус")

        response_search_empty = self.client.get(reverse('tour_list') + '?q=Париж')
        self.assertNotContains(response_search_empty, "Эльбрус")

    def test_contact_view_post(self):
        """Тест отправки формы обратной связи"""
        response = self.client.post(reverse('contacts'), {
            'name': 'Тест',
            'email': 'test@example.com',
            'phone': '+79990001122',
            'message': 'Тестовое сообщение',
            'privacy': True
        })
        self.assertEqual(response.status_code, 302)  # Редирект после успеха
        self.assertEqual(BookingRequest.objects.count(), 1)

    def test_my_tours_requires_login(self):
        """Тест: страница личного кабинета требует авторизации"""
        response = self.client.get(reverse('my_tours'))
        self.assertEqual(response.status_code, 302)  # Редирект на логин
        self.assertIn('/login/', response.url)

    def test_buy_tour_view(self):
        """Тест покупки тура"""
        self.client.login(username="testuser", password="testpassword123")
        # Добавляем карту пользователю
        Card.objects.create(user=self.user, masked_number="**** **** **** 1234")

        response = self.client.post(reverse('buy_tour', args=[self.tour.id]))
        self.assertEqual(response.status_code, 302)  # Редирект в личный кабинет
        self.assertEqual(UserTour.objects.count(), 1)
        self.assertEqual(UserTour.objects.first().status, 'active')