from django.urls import path

from .views import get_historical_data, Analysis, CandleChart

urlpatterns = [
    path('<int:pk>/', get_historical_data, name="get_historical_data"),
    path('<int:pk>/candle-chart/', CandleChart.as_view(), name="candle-chart"),
    path('<int:pk>/analytical-chart/', Analysis.as_view(), name="analytical-chart"),

]