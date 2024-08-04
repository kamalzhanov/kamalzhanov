import schedule
import time
import requests

def get_btc_price():
    print("====BTC===")
    url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    response = requests.get(url)
    data = response.json()
    print(data)
    price = response.get('price')

    """" Стоимость биткоина на текущее время {} , цена {}"""
    print(f' Стоимость биткоина на текущее время {time.ctime()} , цена {price}')

schedule.every(2).seconds.do(get_btc_price)

while True:
    schedule.run_pending()
    

