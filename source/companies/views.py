from django.shortcuts import render
import yfinance as yf
from .models import Company, DailyData

def test(request):
    return render(request, 'base.html')
