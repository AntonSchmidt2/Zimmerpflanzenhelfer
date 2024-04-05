from django.urls import path
from . import views

app_name = 'waterlog'

urlpatterns = [
    path('log/', views.log_watering, name='log_watering'),   # log watering with url
    path('manual_log/', views.log_page, name='manual_log'),  # log watering manually
    path('log-created/', views.add_manual_log, name ='log_added'),  # add manual log
    path('show_logs/', views.show_logs, name='show_logs'),  # show logs
]
