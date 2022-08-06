from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registration, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('portfolio/<str:pid>/', views.portfolioPage, name='portfolio'),
    path('create_port/', views.createPort, name='create_port'),
    path('edit_portfolio/<str:pid>/', views.editPort, name='edit_port'),
]