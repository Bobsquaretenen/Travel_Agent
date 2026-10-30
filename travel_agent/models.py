from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")

    def __str__(self): return self.username


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self): return self.name


class Tour(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название тура")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tours', verbose_name="Категория")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(default=7, verbose_name="Длительность (ночей)")
    image = models.ImageField(upload_to='tours/', blank=True, null=True, verbose_name="Изображение")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"

    def __str__(self): return self.title


class BookingRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    # Делаем поле необязательным
    subject = models.CharField(max_length=50, verbose_name="Тема", null=True, blank=True)
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заявка/Отзыв"
        verbose_name_plural = "Заявки и отзывы"

    def __str__(self): return f"Сообщение от {self.name}"

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards', verbose_name="Пользователь")
    masked_number = models.CharField(max_length=20, verbose_name="Маскированный номер")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата привязки")

    class Meta:
        verbose_name = "Карта"
        verbose_name_plural = "Карты"

    def __str__(self):
        return f"{self.user.username} - {self.masked_number}"


class UserTour(models.Model):
    STATUS_CHOICES = (
        ('active', 'Действующий'),
        ('visited', 'Посещенный'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_tours', verbose_name="Пользователь")
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, verbose_name="Тур")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата покупки")

    class Meta:
        verbose_name = "Купленный тур"
        verbose_name_plural = "Купленные туры"

    def __str__(self):
        return f"{self.user.username} - {self.tour.title} ({self.get_status_display()})"