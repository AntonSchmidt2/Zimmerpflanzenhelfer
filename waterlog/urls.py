from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.log_watering, name='log_watering'),
    path('show_logs/', views.show_logs, name='show_logs'),
]
