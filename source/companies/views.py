from django.shortcuts import render
from .models import Company, DailyData
from .dataloader import DataLoader

def test(request):
    d = DataLoader()
    d.auto_loader()
    return render(request, 'base.html')
