from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, AdminCreateUserForm, ForecastForm
from .models import Forecast, Purchase
from .decorators import admin_required

def home(request):
    latest = Forecast.objects.all()[:3]
    return render(request, 'home.html', {'latest': latest})

def register_view(request):
    if request.user.is_authenticated: return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # пароль хешируется автоматически
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('dashboard')
    else: form = RegisterForm()
    return render(request, 'forecasts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated: return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('dashboard')
        else: messages.error(request, 'Неверное имя пользователя или пароль.')
    else: form = AuthenticationForm()
    return render(request, 'forecasts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    if request.user.is_staff: return redirect('admin_dashboard')
    return redirect('user_dashboard')

@login_required
def user_dashboard(request):
    purchases = Purchase.objects.filter(user=request.user).select_related('forecast')
    return render(request, 'forecasts/user_dashboard.html', {'purchases': purchases})

@login_required
def catalog(request):
    owned_ids = Purchase.objects.filter(user=request.user).values_list('forecast_id', flat=True)
    forecasts = Forecast.objects.all()
    return render(request, 'forecasts/catalog.html', {'forecasts': forecasts,'owned_ids': set(owned_ids),})

@login_required
def buy_forecast(request, pk):
    forecast = get_object_or_404(Forecast, pk=pk)
    obj, created = Purchase.objects.get_or_create(user=request.user, forecast=forecast)
    if created: messages.success(request, f'Услуга «{forecast.title}» успешно приобретена!')
    else: messages.info(request, 'Эта услуга уже есть в вашем кабинете.')
    return redirect('user_dashboard')

@login_required
def forecast_detail(request, pk):
    forecast = get_object_or_404(Forecast, pk=pk)
    has_access = request.user.is_staff or Purchase.objects.filter(user=request.user, forecast=forecast).exists()
    if not has_access:
        messages.error(request, 'Сначала приобретите эту услугу.')
        return redirect('catalog')
    return render(request, 'forecasts/forecast_detail.html', {'forecast': forecast})

#Админка
@admin_required
def admin_dashboard(request):
    forecast_form = ForecastForm()
    user_form = AdminCreateUserForm()

    if request.method == 'POST':
        if 'add_forecast' in request.POST:
            forecast_form = ForecastForm(request.POST, request.FILES)
            if forecast_form.is_valid():
                f = forecast_form.save(commit=False)
                f.author = request.user
                f.save()
                messages.success(request, 'Прогноз успешно загружен.')
                return redirect('admin_dashboard')
        elif 'add_user' in request.POST:
            user_form = AdminCreateUserForm(request.POST)
            if user_form.is_valid():
                user_form.save()  # пароль хешируется
                messages.success(request, 'Пользователь создан.')
                return redirect('admin_dashboard')

    forecasts = Forecast.objects.all()
    return render(request, 'forecasts/admin_dashboard.html', {
        'forecast_form': forecast_form,
        'user_form': user_form,
        'forecasts': forecasts,
    })

@admin_required
def delete_forecast(request, pk):
    forecast = get_object_or_404(Forecast, pk=pk)
    forecast.delete()
    messages.success(request, 'Прогноз удалён.')
    return redirect('admin_dashboard')