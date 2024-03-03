import datetime
from django.shortcuts import render, get_object_or_404
from companies.models import Company, DailyData
from django.views import View
import time
import json

def get_historical_data(request, pk):
    company = get_object_or_404(Company, pk=pk)
    daily_data = DailyData.objects.filter(company=company).order_by('-date')
    title = company.name
    return render(request, 'analytics/historical_data.html',{'title':title,'history': daily_data})

class Analysis(View):


    def get(self, request, pk):
        data_from = request.GET.get('from', None)
        data_to = request.GET.get('to')
        if not data_from:
            data_from = datetime.datetime.now().date() - datetime.timedelta(days=100)
        
        if not data_to:
            data_to = datetime.datetime.now().date()

        company = get_object_or_404(Company, pk=pk)
        daily_data = DailyData.objects.filter(company=company, date__gt=data_from).values('date', 'open', 'high', 'low', 'close')
        
        chart_data = [
            {'x': time.mktime(d['date'].timetuple()),
            'open': d['open'],
            'high': d['high'],
            'low': d['low'],
            'close': d['close'],
            'color': 'green' if d['close'] > d['open'] else 'red'}
            for d in daily_data]
        json_data = json.dumps(list(chart_data))
        print(json_data)
        context =  {
            'data': json_data
        }
        return render(request, 'analytics/candle_chart.html', context=context)

    # def get(self, request, pk):
    #     data_from = request.GET.get('from', None)
    #     data_to = request.GET.get('to')
    #     if not data_from:
    #         data_from = datetime.datetime.now().date() - datetime.timedelta(days=30)
        
    #     if not data_to:
    #         data_to = datetime.datetime.now().date()

    #     company = get_object_or_404(Company, pk=pk)
    #     daily_data = DailyData.objects.filter(company=company, date__gt=data_from).values('date', 'close', 'open')
    #     print(daily_data)
    #     context =  {
    #         'data': daily_data
    #     }
    #     return render(request, 'analytics/default_chart.html', context=context)


