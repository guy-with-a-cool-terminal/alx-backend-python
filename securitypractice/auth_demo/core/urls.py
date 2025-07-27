from django.urls import path
from .views import dashboard,view_reports

urlpatterns =[
    path('dashboard/',dashboard,name='dashboard'),
    path('reports/',view_reports,name='reports'),
]