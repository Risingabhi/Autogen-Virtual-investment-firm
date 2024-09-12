
#this file reads stock symbols which are approx 4500 and then finds their historical data
#data is taken for last 12 months only. to save space and ease of calculation.
# This data is used for further analysis by Investment_Analyst .

# PURPOSE OF THE FILE 

''' We will use CAPM [Captial Asset Pricing Model] for calculating RETURN.
to calculate RISK in each stock, we will look at Standard Deviation.[RISKfor each stock.]

'''


# {'2024-02-15': {'1. open': '30.0800', '2. high': '30.4050', '3. low': '25.5750', '4. close': '27.3900', '5. adjusted close': '27.3900', '6. volume': '61546176', 
# '7. dividend amount': '0.0000'}, 


import threading
import csv
from queue import Queue
import pandas as pd
import requests
import time

def fetch_data(symbol, data_queue):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey=JEVABQILJD0BSD1C"
    #print("url", url)

    r = requests.get(url)
    data = r.json()
    data_as_list = data['Monthly Adjusted Time Series']
    first_12_values = [(key, value) for key, value in list(data_as_list.items())[:12]]
    print(first_12_values)

    data_queue.put((symbol, first_12_values))

def write_to_csv(data_queue):
    with open('symbol_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Adjusted Close', 'Volume', 'Dividend Amount'])

        while True:
            item = data_queue.get()
            if item is None:
                break
            symbol, values = item
            for date, data_dict in values:
                writer.writerow([symbol, date, data_dict['1. open'], data_dict['2. high'], data_dict['3. low'], data_dict['4. close'], data_dict['5. adjusted close'], data_dict['6. volume'], data_dict['7. dividend amount']])
        print("Data written to CSV")
data_queue = Queue()

# Start a thread to write data to CSV
write_thread = threading.Thread(target=write_to_csv, args=(data_queue,))
write_thread.start()

# Start threads to fetch data for each symbol

df = pd.read_csv('./index_data/Invest_indicators_all_stocks.csv')
threads = []
for symbol in df['symbol']:
    time.sleep(0.2)
    thread = threading.Thread(target=fetch_data, args=(symbol, data_queue))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Signal the write thread to finish
data_queue.put(None)
write_thread.join()
