from django.shortcuts import render, get_object_or_404
from companies.models import Company, DailyData

def get_historical_data(request, pk):
    company = get_object_or_404(Company, pk=pk)
    daily_data = DailyData.objects.filter(company=company)
    return render(request, 'analytics/historical_data.html')
