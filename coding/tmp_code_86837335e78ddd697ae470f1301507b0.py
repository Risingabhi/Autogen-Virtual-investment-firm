import yfinance as yf
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries

# Fetching data using yfinance
apple = yf.download('AAPL', start='2022-02-10', end='2022-02-10', interval='1m')

# Fetching data using Alpha Vantage API
api_key = 'KFGE5HXRO7G42KVK'
ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='full')

# Plotting the intraday movement
plt.figure(figsize=(12, 6))
plt.plot(apple.index, apple['Close'], label='yfinance')
plt.plot(data.index, data['4. close'], label='Alpha Vantage')
plt.xlabel('Time')
plt.ylabel('Price')
plt.title('Intraday Movement of Apple Stock')
plt.legend()
plt.show()