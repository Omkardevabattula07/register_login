from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        bio = request.POST.get('bio')
        security_question = request.POST.get('security_question')
        security_answer = request.POST.get('security_answer')
        image = request.FILES.get('image')

        # Security checks
        if password != confirm_password:
            return render(request, 'register.html', {'error': "Passwords do not match"})
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': "Username already exists"})

        # Create user
        user = User.objects.create(username=username, password=make_password(password))
        UserProfile.objects.create(
            user=user,
            bio=bio,
            security_question=security_question,
            security_answer=make_password(security_answer),
            image=image,
        )
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        security_answer = request.POST.get('security_answer')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and check_password(security_answer, user.profile.security_answer):
                login(request, user)
                if user.is_superuser:
                    return redirect('superuser_page')
                return redirect('normal_user_page')
            else:
                return render(request, 'login.html', {'error': "Invalid credentials"})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': "User does not exist"})
    return render(request, 'login.html')

def superuser_page(request):
    users = User.objects.all()
    return render(request, 'superuser.html', {'users': users})

def normal_user_page(request):
    users = User.objects.all()
    return render(request, 'user.html', {'users': users})
