
import matplotlib as plt
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
import os
import requests

def plot_monthly_index_movement(index_symbol, start_date, end_date):
    """
    Plot the monthly index movement for a given period using Plotly and save the data to a CSV file.
    
    Parameters:
        index_symbol (str): Symbol of the index (e.g., "^GSPC" for S&P 500, "^IXIC" for NASDAQ).
        start_date (str): Start date for the period in 'YYYY-MM-DD' format.
        end_date (str): End date for the period in 'YYYY-MM-DD' format.
    """
    # Fetch the historical data for the index
    index_data = yf.download(index_symbol, start=start_date, end=end_date)
    
    # Check if the data is empty
    if index_data.empty:
        print(f"{index_symbol}: No price data found, symbol may be delisted or incorrect (1d {start_date} -> {end_date})")
        return
    
    # Resample the data to get the last price of each month
    monthly_data = index_data.resample('M').last()
    
    # Calculate monthly movements
    monthly_data['Monthly Movement'] = monthly_data['Close'].pct_change() * 100
    
    # Ensure the directory exists
    directory = "index_data"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Define the CSV file path
    csv_file_path = os.path.join(directory, f"{index_symbol}_monthly_data_{start_date}_to_{end_date}.csv")
    
    # Save the monthly data to CSV
    monthly_data.to_csv(csv_file_path)
    print(f"Data saved to {csv_file_path}")
    
    # Create a Plotly bar chart
    fig = go.Figure(data=[go.Bar(x=monthly_data.index, y=monthly_data['Monthly Movement'])])
    
    # Customize layout
    fig.update_layout(title=f'Monthly Movement for {index_symbol} ({start_date} to {end_date})',
                      xaxis_title='Month',
                      yaxis_title='Percentage Movement',
                      template='plotly_dark')
    
    # Show plot
    fig.show()

# # Example usage
# plot_monthly_index_movement("^GSPC", "2023-01-01", "2023-12-31")

import threading
import csv
from queue import Queue
import pandas as pd
import requests
import time




# #this function gets the BETA value of stock by pulling information from the newtonanalytics.
# def get_beta(smbl,data_beta_queue):
#     url = f'https://api.newtonanalytics.com/stock-beta/?ticker={smbl}&index={smbl}&interval=1mo​&observations=10'

#     r = requests.get(url)
#     data = r.json()
#     #print(smbl,data['data'])
#     data_beta_queue.put((smbl,data['data']))

# def writebeta_to_csv(data_beta_queue):
#     df = pd.read_csv('symbol_data.csv')
#     # Add a new column for Beta with default value ''
#     df['Beta'] = None

#     while True:
#         item = data_beta_queue.get()
#         if item is None:
#             break
#         smbl, beta_value = item
#         print("beta_value",beta_value)
#         df.loc[df['Symbol'] == smbl, 'Beta'] = beta_value
#          # Write the updated DataFrame back to the CSV file
#         df.to_csv('symbol_data.csv', index=False)

#     print("Data written to CSV")
# data_beta_queue = Queue()
# # Start a thread to write data to CSV
# write_thread = threading.Thread(target=writebeta_to_csv, args=(data_beta_queue,))
# write_thread.start()

# # Start threads to fetch data for each symbol

# df = pd.read_csv('../index_data/Invest_indicators_all_stocks.csv')
# threads = []
# for smbl in df['symbol']:
#     time.sleep(0.2)
#     thread = threading.Thread(target=get_beta, args=(smbl, data_beta_queue))
#     thread.start()
#     threads.append(thread)

# # Wait for all threads to finish
# for thread in threads:
#     thread.join()

# # Signal the write thread to finish
# data_beta_queue.put(None)
# write_thread.join()

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
# Importing libraries and packages
import statsmodels.api as sm
from statsmodels import regression

# Importing python package pandas datareader to import data from yahoo
from pandas_datareader import data as pdr
import yfinance as yf

def get_alpha_beta(df2, df):
    alpha_beta_dict = {}
    for smbl in df['symbol']:
        try:
            yf.pdr_override()
            df1 = pdr.get_data_yahoo(smbl, start="2020-01-01", end="2024-02-1")
            return_stock = df1.Close.pct_change()[1:]
            return_spy = df2.Close.pct_change()[1:]

            # Check if lengths of return_stock and return_spy match
            if len(return_stock) != len(return_spy):
                print(f"Lengths of return_stock ({len(return_stock)}) and return_spy ({len(return_spy)}) do not match for symbol {smbl}")
                continue

            X, Y = return_spy.values, return_stock.values
            alpha, beta = linreg(X, Y)

            alpha_beta_dict[smbl] = {'Alpha': alpha, 'Beta': beta}
        except Exception as e:
            print(f"Error processing symbol {smbl}: {e}")

    return alpha_beta_dict


def linreg(x, y):
    x = sm.add_constant(x)
    model = regression.linear_model.OLS(y, x).fit()
    x = x[:, 1]
    return model.params[0], model.params[1]

# Assuming df is your DataFrame with symbols
df = pd.read_csv('../index_data/Invest_indicators_all_stocks.csv')
# Calculate S&P 500 returns
yf.pdr_override()
df2 = pdr.get_data_yahoo("SPY", start="2020-01-01", end="2024-02-1")

alpha_beta_dict = get_alpha_beta(df2, df)

# Convert the dictionary to a DataFrame
alpha_beta_df = pd.DataFrame.from_dict(alpha_beta_dict, orient='index')
# Save the DataFrame to a CSV file
alpha_beta_df.to_csv('alpha_beta_data.csv')
print("Data written to alpha_beta_data.csv")
