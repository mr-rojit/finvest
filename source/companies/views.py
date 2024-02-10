from django.shortcuts import render
from .models import Company, DailyData
from .dataloader import DataLoader

def home_page(request):
    companies = Company.objects.all()
    for c in companies:
        data = DailyData.objects.filter(company=c).order_by('-date')[:2]
        change = (data[0].close - data[1].close)
        percentage_change = change / data[1].close
        c.change= change
        c.percentage_change = percentage_change

    return render(request, 'home/home.html',{'companies':companies} )
