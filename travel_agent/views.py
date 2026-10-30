from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tour, Card, UserTour, Category
from .forms import CustomUserCreationForm, CustomLoginForm, BookingRequestForm, CardForm
from django.core.exceptions import PermissionDenied
from django.db.models import Q

def home(request):
    tours = Tour.objects.filter(is_active=True)[:6]
    return render(request, 'main.html', {'tours': tours})


def tour_list(request):
    query = request.GET.get('q', '')
    tours = Tour.objects.filter(is_active=True)

    if query:
        tours = tours.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    return render(request, 'travel.html', {
        'tours': tours,
        'query': query
    })

def info_view(request):
    return render(request, 'information.html')


def contact_view(request):
    if request.method == 'POST':
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            # Сохраняем в память, но не в БД (commit=False)
            booking = form.save(commit=False)
            # Задаем тему по умолчанию
            booking.subject = "Отзыв с сайта"
            booking.save()

            messages.success(request, "Спасибо! Ваш отзыв отправлен.")
            return redirect('contacts')
    else:
        form = BookingRequestForm()
    return render(request, 'contacts.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ИСПРАВЛЕНО: явно указываем, какой бэкенд использовать
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Регистрация прошла успешно! Добро пожаловать.")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'logup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Вы успешно вошли в аккаунт.")
            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect('home')


@login_required
def my_tours_view(request):
    user_tours = UserTour.objects.filter(user=request.user).order_by('-purchase_date')
    active_tours = user_tours.filter(status='active')
    visited_tours = user_tours.filter(status='visited')
    cards = Card.objects.filter(user=request.user)

    return render(request, 'my_tours.html', {
        'active_tours': active_tours,
        'visited_tours': visited_tours,
        'cards': cards
    })


@login_required
def add_card_view(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            masked = f"**** **** **** {number[-4:]}"
            Card.objects.create(user=request.user, masked_number=masked)
            messages.success(request, "Карта успешно привязана!")
            return redirect('my_tours')
    else:
        form = CardForm()
    return render(request, 'add_card.html', {'form': form})


@login_required
def buy_tour_view(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    # Проверяем, есть ли у пользователя карта
    if not Card.objects.filter(user=request.user).exists():
        messages.warning(request, "Для оплаты сначала привяжите карту.")
        return redirect('add_card')

    if request.method == 'POST':
        # Имитация успешной оплаты
        UserTour.objects.create(user=request.user, tour=tour, status='active')
        messages.success(request, f"Тур «{tour.title}» успешно оплачен!")
        return redirect('my_tours')

    return render(request, 'buy_tour.html', {'tour': tour})


@login_required
def complete_tour_view(request, usertour_id):
    user_tour = get_object_or_404(UserTour, id=usertour_id, user=request.user)
    user_tour.status = 'visited'
    user_tour.save()
    messages.success(request, f"Тур «{user_tour.tour.title}» перенесен в посещенные!")
    return redirect('my_tours')

def csrf_failure(request, reason=""):
    """Обработчик ошибки CSRF (вызывается вместо стандартной желтой страницы)"""
    return render(request, '403.html', status=403)

def exception_403(request, exception=None):
    """Обработчик ошибки 403 Доступ запрещен"""
    return render(request, '403.html', status=403)

def exception_404(request, exception=None):
    """Обработчик ошибки 404 Страница не найдена"""
    categories = Category.objects.all()
    return render(request, '404.html', {'categories': categories}, status=404)

def exception_500(request):
    """Обработчик ошибки 500 Внутренняя ошибка сервера"""
    return render(request, '500.html', status=500)

# --- ТЕСТОВАЯ ФУНКЦИЯ ДЛЯ ПРОВЕРКИ ---
def test_403_view(request):
    """Вызывает ошибку 403 для проверки"""
    from django.core.exceptions import PermissionDenied
    raise PermissionDenied