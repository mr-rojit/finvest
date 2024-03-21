import datetime
from django.shortcuts import render, get_object_or_404
from companies.models import Company, DailyData
from django.views import View
import time
import json
from ta.volatility import BollingerBands
from ta.momentum import ROCIndicator, AwesomeOscillatorIndicator, KAMAIndicator
from ta.volume import OnBalanceVolumeIndicator
import pandas as pd

def get_historical_data(request, pk):
    company = get_object_or_404(Company, pk=pk)
    daily_data = DailyData.objects.filter(company=company).order_by('-date')
    title = company.name
    return render(request, 'analytics/historical_data.html',{'title':title,'history': daily_data})


class Analysis(View):

    def roc_indicator(self, data):
        df = pd.DataFrame(data)
        roc = ROCIndicator(df['close'])
        return list(roc.roc())
    
    def awesome_oscillator(self, data):
        # AwesomeOscillatorIndicator(data)
        pass

    def on_balance_volume(self, data):
        df = pd.DataFrame(data)
        obv = OnBalanceVolumeIndicator(df['close'], df['volume'])
        return list(obv.on_balance_volume())


    def get(self, request, pk):
        data_from = request.GET.get('from', None)
        data_to = request.GET.get('to')
        analysis_type = request.GET.get('analysis',None)
        if not data_from:
            data_from = datetime.datetime.now().date() - datetime.timedelta(days=30)
        
        if not data_to:
            data_to = datetime.datetime.now().date()

        company = get_object_or_404(Company, pk=pk)
        daily_data = DailyData.objects.filter(company=company, date__gt=data_from).values('date', 'open', 'close', 'volume')

        analytics_data = []
        analytics_name = None

        if analysis_type and analysis_type == 'roc':
            roc = self.roc_indicator(daily_data)
            analytics_name = 'ROC Indicator'
            for i,j in zip(daily_data, roc):
                analytics_data.append({'date': i['date'], 'indicator': j})

        elif analysis_type and analysis_type == 'kama':
            pass
        
        elif analysis_type and analysis_type == 'obv':
            obv = self.on_balance_volume(daily_data)
            analytics_name = 'On Balance Volume Indicator'
            for i,j in zip(daily_data, obv):
                analytics_data.append({'date': i['date'], 'indicator': j})


        context =  {
            'data': daily_data,
            'ta_data': analytics_data,
            'analytics_name': analytics_name
        }
        return render(request, 'analytics/default_chart.html', context=context)





class CandleChart(View):

    def get(self, request, pk):
        data_from = request.GET.get('from', None)
        data_to = request.GET.get('to')
        if not data_from:
            data_from = datetime.datetime.now().date() - datetime.timedelta(days=30)
        
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
            'data': json_data,
            'company': company
        }
        return render(request, 'analytics/candle_chart.html', context=context)
    
