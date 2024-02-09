from .models import Company

companies = {
    'AAPL': 'Apple Inc.',
    'GOOG':'Alphabet Inc.',
    'MSFT':'Microsoft Corporation',
    'AMZN':'Amazon.com, Inc.',
    'META':'Meta Platforms, Inc.',
    'ARM':'Arm Holdings plc',
    'NFLX':'Netflix, Inc.',
    'ORCL':'Oracle Corporation',
    'TSLA':'Tesla, Inc.',
    'NVDA':'NVIDIA Corporation',
    'BABA':'Alibaba Group Holding Limited',
    'CRM':'Salesforce, Inc.',
    'PYPL':'PayPal Holdings, Inc.',
    'INTC':'Intel Corporation'

}

def manual_populate_companies():
    for k,v in companies.items():
        Company.objects.get_or_create(symbol=k, name=v, defaults={'status':True})
