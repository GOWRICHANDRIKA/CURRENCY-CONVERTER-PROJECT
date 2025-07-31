import requests
from flask import Flask, render_template, request
app = Flask(__name__)
currencies = [
    'USD', 'EUR', 'GBP', 'INR', 'AUD', 'CAD', 'SGD', 'CHF', 'MYR', 'JPY', 'CNY','EUR','BDT','BBD','IRR','KRW','MXN','PKR','RUB','SEK','TRY',
    'VND','KPW','ZWL','ZAR','JMD','LKR','NZD','NPR','NOK','NGN','NGN','AFN','ANG','BRL','BTN','COP','HKD','IDR','ILS','IQD','BMD','BKK','EGP',
    'EUR','DKK','FJD','EUR','GHS','EUR','HGF','JOD','EUR','KZT','KES','PEN','PHP','PLN','EUR','QAR','RON','SAR','RWF','XOF','RSD','EUR','TWD',
    'SZL','THB','UGX','UAH','UZS','ZMW','VEF','TMT','AOA','AMD','EUR','AZN','BHD','BYN','BOB','BAM','BWP','BRL','BGN','CVE','KHR','XAF','CLP',
    'KYD','CDF','CRC','HRK','EUR','DOP','XAF'
   ]
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        amount = request.form.get('amount')
        from_currency = request.form.get('from_currency')
        to_currency = request.form.get('to_currency')
        result2=1

        if not amount or not from_currency or not to_currency:
            return render_template('index.html', currencies=currencies, error='Please fill out all fields.')

        try:
            amount = float(amount)
        except ValueError:
            return render_template('index.html', currencies=currencies, error='Invalid amount.')

        api_key = '77d25452491d42d38ca738a3b73da383'
        url = f'https://openexchangerates.org/api/latest.json?app_id={api_key}'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if 'rates' not in data:
                return render_template('index.html', currencies=currencies, error='Rates not found in API response.')
        except requests.exceptions.RequestException as e:
            return render_template('index.html', currencies=currencies, error=f'Error accessing API: {str(e)}')
        except ValueError as e:
            return render_template('index.html', currencies=currencies, error=f'Error parsing JSON: {str(e)}')

        from_rate = data['rates'].get(from_currency)
        to_rate = data['rates'].get(to_currency)
    

        if not from_rate or not to_rate:
            return render_template('index.html', currencies=currencies, error='Invalid currency selection.')

        converted_amount = (amount / from_rate) * to_rate


        return render_template('index.html',unit=to_rate, currencies=currencies, result=f'{amount} {from_currency} = {converted_amount} {to_currency}',k=f'1 {from_currency} = {to_rate} {to_currency}')

    return render_template('index.html', currencies=currencies)

if __name__ == '__main__':
    app.run(debug=True)

