from django.shortcuts import render
import yfinance as yf

def test(request):
    return render(request, 'base.html')
