from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registration, name='register'),
    path('logout', views.logoutUser, name='logout')
]