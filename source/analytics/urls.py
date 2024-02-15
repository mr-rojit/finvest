from django.urls import path

from .views import get_historical_data, Analysis

urlpatterns = [
    path('<int:pk>/', get_historical_data, name="get_historical_data"),
    path('<int:pk>/chart/', Analysis.as_view(), name="analysis"),
]