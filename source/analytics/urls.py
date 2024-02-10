from django.urls import path

from .views import get_historical_data

urlpatterns = [
    path('<int:pk>/', get_historical_data, name="get_historical_data")
]