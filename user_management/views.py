from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Неудачная попытка входа
            messages.error(request, 'Неверный email или пароль.')
    return render(request, 'backend/auth-sign-in.html')

def logout_view(request):
    logout(request)
    # Redirect to a specific page after logout
    return redirect('login')  # Change 'login' to your login URL name

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        confirm_password = request.POST['password2']

        # Проверка совпадения паролей
        if password != confirm_password:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('register')

        # Проверка уникальности email
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким username уже зарегистрирован.')
            return redirect('register')

        # Создание нового пользователя
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Автоматический вход после регистрации
        login(request, user)

        # Редирект на главную страницу
        return redirect('home')
    return render(request, 'backend/auth-sign-up.html')

def user_profile_view(request):
    user_profile = User.objects.get(pk=request.user.pk)
    return render(request, 'app/user-profile.html', {'user_profile': user_profile})