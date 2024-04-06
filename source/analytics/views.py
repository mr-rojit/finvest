import datetime
from django.shortcuts import render, get_object_or_404
from companies.models import Company, DailyData
from django.views import View
import time
import json
from ta.volatility import BollingerBands
from ta.momentum import ROCIndicator, AwesomeOscillatorIndicator, KAMAIndicator, PercentageVolumeOscillator, StochasticOscillator
from ta.volume import OnBalanceVolumeIndicator
import pandas as pd

from statsmodels.tsa.arima.model import ARIMA

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

    def bollinger_bands(self, data):
        df = pd.DataFrame(data)
        bb = BollingerBands(df['close'])
        return list(bb.bollinger_mavg())
    
    def stochastic_osc(self, data):
        df = pd.DataFrame(data)
        sto_osc = StochasticOscillator(df['close'], df['high'], df['low'])
        return list(sto_osc.stoch())
    
    def awesome_oscillator(self, data):
        df = pd.DataFrame(data)
        awesome_osc = AwesomeOscillatorIndicator(df['high'], df['low'])
        return list(awesome_osc.awesome_oscillator())

    def on_balance_volume(self, data):
        df = pd.DataFrame(data)
        obv = OnBalanceVolumeIndicator(df['close'], df['volume'])
        return list(obv.on_balance_volume())

    def percentile_volume_osc(self, data):
        df = pd.DataFrame(data)
        pvo = PercentageVolumeOscillator(df['close'])
        return list(pvo.pvo_hist())


    def get(self, request, pk):
        data_from = request.GET.get('from', None)
        data_to = request.GET.get('to', None)
        analysis_type = request.GET.get('analysis',None)
        if not data_from:
            data_from = datetime.datetime.now().date() - datetime.timedelta(days=90)
        
        if not data_to:
            data_to = datetime.datetime.now().date()

        company = get_object_or_404(Company, pk=pk)
        is_prediction_available = False
        if company.symbol in ['MSFT', 'GOOG', 'AAPL', 'AMZN']:
            is_prediction_available = True
        daily_data = DailyData.objects.filter(company=company, date__gt=data_from, date__lte=data_to).values('date', 'open', 'high', 'low', 'close', 'volume')
        test_data = list(reversed(DailyData.objects.filter(company=company).values('close')))[:10]
        x = []
        for i in test_data:
            x.append(i['close'])
        
        for w in range(2):
            trend_value = 0

            for i in range(len(x)-1):
                trend_value += (x[i] - x[i+1])
            if w == 1:
                pred = (trend_value/10)+x[0]
            else:
                pred = (trend_value)+x[0]
            x.insert(0, pred)

        #

        last_date = daily_data.last()['date']
        next_day_1 = last_date + datetime.timedelta(days=1)
        next_day_2 = last_date + datetime.timedelta(days=2)

        new_pred = list(DailyData.objects.filter(company=company, date__gt=last_date - datetime.timedelta(days=10)).values('date','close'))
        new_pred.append({'date':next_day_1, 'close': x[1] })
        new_pred.append({'date':next_day_2, 'close': x[0] })
        #

        
        analytics_data = []
        analytics_name = None

        if analysis_type and analysis_type == 'roc':
            roc = self.roc_indicator(daily_data)
            analytics_name = 'ROC Indicator'
            for i,j in zip(daily_data, roc):
                analytics_data.append({'date': i['date'], 'indicator': j})

        elif analysis_type and analysis_type == 'bb':
            bb = self.bollinger_bands(daily_data)
            analytics_name = 'Bollinger MAVG'
            for i,j in zip(daily_data, bb):
                analytics_data.append({'date': i['date'], 'indicator': j})

        elif analysis_type and analysis_type == 'awesomeOsc':
            awesome_osc = self.awesome_oscillator(daily_data)
            analytics_name = 'Awesome Osciallator'
            for i,j in zip(daily_data, awesome_osc):
                analytics_data.append({'date': i['date'], 'indicator': j})

        elif analysis_type and analysis_type == 'stoOsc':
            sto_osc = self.stochastic_osc(daily_data)
            analytics_name = 'Stochastic Osciallator'
            for i,j in zip(daily_data, sto_osc):
                analytics_data.append({'date': i['date'], 'indicator': j})

        elif analysis_type and analysis_type == 'obv':
            obv = self.on_balance_volume(daily_data)
            analytics_name = 'On Balance Volume Indicator'
            for i,j in zip(daily_data, obv):
                analytics_data.append({'date': i['date'], 'indicator': j})
        
        elif analysis_type and analysis_type == 'pvo':
            pvo = self.percentile_volume_osc(daily_data)
            analytics_name = 'Percentile Volume Oscillator'
            for i,j in zip(daily_data, pvo):
                analytics_data.append({'date': i['date'], 'indicator': j})



        context =  {
            'data': daily_data,
            'ta_data': analytics_data,
            'analytics_name': analytics_name,
            'new_pred': new_pred,
            'company': company,
            'is_prediction_available': is_prediction_available
        }
        return render(request, 'analytics/default_chart.html', context=context)





class CandleChart(View):

    def get(self, request, pk):
        data_from = request.GET.get('from', None)
        data_to = request.GET.get('to')
        if not data_from:
            data_from = datetime.datetime.now().date() - datetime.timedelta(days=60)
        
        if not data_to:
            data_to = datetime.datetime.now().date()

        company = get_object_or_404(Company, pk=pk)
        daily_data = DailyData.objects.filter(company=company, date__gt=data_from,date__lte=data_to).values('date', 'open', 'high', 'low', 'close')


        chart_data = [
            {'x': time.mktime(d['date'].timetuple()),
            'open': d['open'],
            'high': d['high'],
            'low': d['low'],
            'close': d['close'],
            'color': 'green' if d['close'] > d['open'] else 'red'}
            for d in daily_data]
        json_data = json.dumps(list(chart_data))

        context =  {
            'data': json_data,
            'company': company
        }
        return render(request, 'analytics/candle_chart.html', context=context)
    
