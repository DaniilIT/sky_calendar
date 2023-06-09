from django.urls import path

from core import views

urlpatterns = [
    path('signup', views.UserCreateView.as_view(), name='signup'),
    path('login', views.LoginView.as_view(), name='login'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('update_password', views.PasswordUpdateView.as_view(), name='update_password'),
]
