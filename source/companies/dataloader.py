import datetime
import yfinance as yf
from .models import Company, DailyData
class DataLoader:

    def auto_loader(self):
        today = datetime.datetime.today().date()
        companies = Company.objects.all()
        for company in companies:
            start_date = None
            if not DailyData.objects.filter(company=company).exists():
                start_date = '2010-01-01'
            else:
                last_date = DailyData.objects.filter(company=company).last().date
                start_date = last_date + datetime.timedelta(1)
            stocks = yf.download(company.symbol, start=start_date, end=today)
            if len(stocks) > 0:
                for index, row in stocks.iterrows():
                    DailyData.objects.create(
                            company=company,
                            date=index,
                            open=row['Open'],
                            high=row['High'],
                            low=row['Low'],
                            close=row['Close'],
                            volume=row['Volume'],
                        )