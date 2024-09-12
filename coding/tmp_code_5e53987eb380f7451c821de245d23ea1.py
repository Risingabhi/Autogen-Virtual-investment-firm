import yfinance as yf
import matplotlib.pyplot as plt

# Fetching Apple's stock data from Yahoo Finance
apple = yf.Ticker("AAPL")
data = apple.history(period="1y")

# Calculating Year-over-Year (YOY) percentage change
data['YOY'] = data['Close'].pct_change(periods=252) * 100

# Plotting the YOY movement
plt.figure(figsize=(10, 6))
plt.plot(data.index, data['YOY'], color='blue')
plt.title("Year-over-Year (YOY) Movement of Apple's Stock Price")
plt.xlabel("Date")
plt.ylabel("YOY Percentage Change")
plt.grid(True)
plt.show()