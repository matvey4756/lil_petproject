import requests
import json
from datetime import datetime
from pprint import pprint

def get_currency_rates():
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            currencies_of_interest = ['USD', 'EUR', 'CZK', 'CHF']
            rates = {}
            for currency in currencies_of_interest:
                if currency in data['Valute']:
                    rates[currency] = {
                        'name': data['Valute'][currency]['Name'],
                        'rate': data['Valute'][currency]['Value'],
                        'nominal': data['Valute'][currency]['Nominal']
                        }
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'date': data['Date'],
                'base_currency': 'RUB',
                'rates': rates
            }
            
            return result
        
        else:
            print(f"Ошибка API: {response.status_code}")
            return None
        

def save_to_json(data, filename='currency_history.json'):
    try:
        with open(filename, 'r', encoding='utf-8')as f:
            history = json.load(f)
    except(FileExistsError, json.JSONDecodeError):
        history = []
        
    history.append(data)
    
    with open(filename, 'w', encoding='utf-8')as f:
        json.dump(history, f, indent=2, ensure_ascii=False)
        print(f"✅ Сохранено в {filename}")
        
        
if __name__ == "__main__":
    currency_data = get_currency_rates()
    if currency_data:
        save_to_json(currency_data)
        print('Данные успешно сохранены')
    else:
        print('Что-то пошло не так(')