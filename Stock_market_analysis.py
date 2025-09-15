import requests,time
from datetime import datetime
from datetime import timedelta
from datetime import date
import pandas as pd


def date_to_timestamp(date):
    time_tuple = date.timetuple()
    timestamp = round(time.mktime(time_tuple))
    return timestamp

def timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp)

def parameters():
    global start,end,freq
    # Previous day
    start = date_to_timestamp(date.today()-timedelta(3))
    # end = date_to_timestamp(date.today()-timedelta(1))
    # Current day
    # start = date_to_timestamp(datetime.today())
    end = date_to_timestamp(datetime.today())
    freq = 60

def process():
    intraday_data = []
    sectors = ['HEALTHCARE','MATERIALS','REAL ESTATE','CONSUMER STAPLES','CONSUMER DISCRETIONARY',\
                'UTILITIES','ENERGY','INDUSTRIALS','CONSUMER SERVICES','FINANCIALS','TECHNOLOGY']
        
    stock = ['RELIANCE','INFY','PAYTM','ISEC']
    
    for company in stock:
        avail = False
        url = 'https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol='+company+'&resolution='+str(freq)+'&from='+str(start)+'&to='+str(end)+'&countback=300&currencyCode=INR'
        company_dict = {'cp':company}
        # print(url)
        print("Stock ", company)
        resp = 'No_data'
        try:
            resp = requests.get(url).json()
            # print(resp['s'])
            resp.update(company_dict)
            data = pd.DataFrame(resp)
            avail = True
        except:
            # no-_data
            data = pd.DataFrame(resp,index=[0])
            intraday_data = data
        date = []
        # print(data)
        
        if avail == True:
            for dt in data['t']:
                date.append({'Date':timestamp_to_date(dt)})
            
            dt = pd.DataFrame(date)
            # print(dt)
            intraday_data = pd.concat([data['cp'],dt,data['o'],data['h'],data['l'],data['c'],data['v']],axis=1)\
                .rename(columns={'cp':'Company','o':'Open','h':'High','l':'Low','c':'Close','v':'Volume'})
        print(intraday_data)

def main():
    parameters()
    process()
    
if __name__ == '__main__':
    main()