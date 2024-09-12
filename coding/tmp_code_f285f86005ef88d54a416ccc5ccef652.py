import yfinance as yf
import matplotlib.pyplot as plt

# Fetching the stock data
nvda = yf.download("NVDA", start="2019-01-01", end="2021-01-01")
tesla = yf.download("TSLA", start="2019-01-01", end="2021-01-01")

# Plotting the stock prices
plt.figure(figsize=(12, 6))
plt.plot(nvda['Close'], label='NVDA')
plt.plot(tesla['Close'], label='TSLA')
plt.title('NVDA vs TSLA Stock Prices')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()