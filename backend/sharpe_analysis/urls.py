from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registration, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('portfolio/<str:pid>/', views.portfolioPage, name='portfolio'),
    path('edit_portfolio/<str:pid>/', views.editPort, name='edit_port'),
    path('delete_port/<str:pid>/', views.del_port, name='del_port'),
    path('del_sec/<str:sid>/<str:pid>/', views.del_sec, name='del_sec'),
    path('analyze/<str:pid>/', views.analyze, name='analyze'),
]