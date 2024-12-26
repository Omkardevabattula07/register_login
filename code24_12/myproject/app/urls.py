from django.urls import path
from . import views

urlpatterns = [
     path('', views.base, name='base'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('superuser/', views.superuser_page, name='superuser_page'),
    path('normal/', views.normal_user_page, name='normal_user_page'),
]
