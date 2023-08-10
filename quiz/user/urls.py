from django.urls import path
from .views import UserRegisterView,HomePageView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',UserRegisterView.as_view(),name='register'),
    path('',HomePageView.as_view(),name='home'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


]

