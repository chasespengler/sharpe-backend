from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('get-stats/<str:pk>/', views.getStats, name='get-stats'),
    path('post-stats/', views.postStats, name='post-stats'),
    path('update-stats/<str:pk>/', views.updateStats, name='update-stats'),
    path('delete-stats/<str:pk>/', views.deleteStats, name='delete-stats'),
    path('exists/<str:pk>/', views.existStats, name='sec-exists'),
]