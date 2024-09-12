#this file defines the investment objectives for the investment_analyst.
import requests
import json

import csv
import pandas as pd
import time



# investment_paramters = {"Market_cap_Segment": ["Large","Mid","small"],
# "Sector_Industry": "",
# "Financial": ["Earnings Growth", "Profit_margin","debt-equity-ratio"],
# "Valuation_metrics":"P/E_ratio",
# "Dividend_Yield": "",
# "Technical_indicators":["52week_high_low","Moving_average","Relative_strength_index"],
# }

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key



# sector_query_list =["technology","blockchain","energy_transportation","finance","life_sciences","manufacturing","real_estate","retail_wholesale"]

# for sector in sector_query_list:
# 	url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics={sector}&apikey=JEVABQILJD0BSD1C'
# 	r = requests.get(url)
# 	data = r.json()


# details = data['feed']



# ticker_details =[] #its a tuple/ (tckr,sector_info)
# for element in details:
# 	tckr =("ticker_details", element['ticker_sentiment'])
# 	sector_info = element['topics'][0]['topic']
# 	ticker_details.append((tckr,sector_info))



# # Assuming ticker_details is your list of tuples containing the data

# # Open a CSV file in write mode
# with open('ticker_details.csv', 'w', newline='') as csvfile:
#     # Create a CSV writer object
#     csv_writer = csv.writer(csvfile)
    
#     # Write header row
#     csv_writer.writerow(['Script Symbol', 'Market Sentiment Score', 'Sector'])
    
#     # Iterate through each tuple in ticker_details
#     for exact_details in ticker_details:
#         tckr_, sctr_ = exact_details  # extract values from tuple
#         print("tckr",type(tckr))
#         x,script_symbol = tckr_  # this is ticker symbol 
#         print(x)
#         print("ssymbo",script_symbol)
#         script_code = script_symbol[0]['ticker']
#         market_sentiment_score = script_symbol[0]['ticker_sentiment_score']
#         sector = sctr_  # sector value
        
#         # Write the values to the CSV file
#         csv_writer.writerow([script_code, market_sentiment_score, sector])




#get all actively traded stocks this code doesnt work, simply paste url on browser and it gives csv file of all listed stocks,
# url2 = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=JEVABQILJD0BSD1C'

# results = requests.get(url2)

# print("complete",results)



# Read the CSV file into a pandas DataFrame
'''function to get information about stocks listed below:'''
 # fundamentals = [
 #        "EBITDA", "PERatio", "PEGRatio", "DividendPerShare",
 #        "DividendYield", "EPS", "RevenuePerShareTTM", "ProfitMargin",
 #        "OperatingMarginTTM", "ReturnOnAssetsTTM", "ReturnOnEquityTTM",
 #        "RevenueTTM", "GrossProfitTTM", "DilutedEPSTTM",
 #        "QuarterlyEarningsGrowthYOY", "QuarterlyRevenueGrowthYOY",
 #        "AnalystTargetPrice", "TrailingPE", "ForwardPE",
 #        "PriceToSalesRatioTTM", "PriceToBookRatio", "EVToRevenue",
 #        "EVToEBITDA", "Beta", "52WeekHigh", "52WeekLow",
 #        "50DayMovingAverage", "200DayMovingAverage"
 #    ]
    

# #items removed as many parameters are not presnt.
# def get_allinfo_for_ticker():
#     # Define the list of fundamentals
#     fundamentals = [
#         "PERatio", "DividendPerShare",
#         "DividendYield", "EPS", "ProfitMargin","PriceToBookRatio"
#          "Beta", "52WeekHigh", "52WeekLow",
#         "50DayMovingAverage", "200DayMovingAverage"
#     ]
    
#     # Read the existing CSV file into a DataFrame
#     df = pd.read_csv('./nyse_active_stocks/test.csv')
    
#     # Create an empty list to store the dictionaries of fundamental values
#     fundamental_values_list = []
    
#     # Iterate over each symbol
#     for symbol in df['symbol']:
#         try:
#             url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey=JEVABQILJD0BSD1C' #pulls fundamentals/
#             r = requests.get(url)
#             data = r.json()

            
            
#             # Initialize a dictionary to store the fundamental values for this symbol
#             fundamental_values = {'symbol': symbol}
            
#             # Iterate over each fundamental
#             for funda in fundamentals:
#                 # Try to retrieve the value for the fundamental
#                 new_value = data.get(funda, 'NA')
#                 print("working to get data for all tickers", new_value)
                
#                 # Store the value in the dictionary
#                 fundamental_values[funda] = new_value
                
#                 time.sleep(0.2)  # Adding a delay to avoid hitting API rate limits
            
#             # Append the dictionary to the list
#             fundamental_values_list.append(fundamental_values)
            
#         except Exception as e:
#             print(f"Error occurred for symbol {symbol}: {e}")
    
#     # Convert the list of dictionaries into a DataFrame
#     new_df = pd.DataFrame(fundamental_values_list)
    
#     # Add 'symbol' column to the DataFrame
#     new_df['symbol'] = df['symbol']
    
#     # Concatenate the existing DataFrame with the new DataFrame
#     final_df = pd.concat([df, new_df], axis=1)
    
#     # Save the DataFrame to a new CSV file
#     final_df.to_csv('final_list_active_stocks_with_fundamentals.csv', index=False)

# # Call the function
# get_allinfo_for_ticker()






# for key,val in data.items():
# 	print(key)

#for pulling techincal indicators. 
            #simple_moving_average for 60 day period basis open price.
            # SMA_url = f'https://www.alphavantage.co/query?function=SMA&symbol={symbol}&interval=monthly&time_period=10&series_type=open&apikey=JEVABQILJD0BSD1C'
            # s = requests.get(SMA_url)
            # data_sma = s.json()
            # print("data_sma",data_sma)


import pandas as pd
import requests
import threading

def get_fundamentals_for_symbol(symbol, fundamentals, fundamental_values_list):
    try:
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey=JEVABQILJD0BSD1C' #pulls fundamentals/
        r = requests.get(url)
        data = r.json()


        # Initialize a dictionary to store the fundamental values for this symbol
        fundamental_values = {'symbol': symbol}

        # Iterate over each fundamental
        for funda in fundamentals:
            # Try to retrieve the value for the fundamental
            new_value = data.get(funda, 'NA')
            print("working to get data for all tickers", new_value)

            # Store the value in the dictionary
            fundamental_values[funda] = new_value

        # Append the dictionary to the list
        fundamental_values_list.append(fundamental_values)
    except Exception as e:
        print(f"Error occurred for symbol {symbol}: {e}")

def get_allinfo_for_ticker():
    # Define the list of fundamentals
    fundamentals = [
        "PERatio", "DividendPerShare",
        "DividendYield", "EPS", "ProfitMargin","PriceToBookRatio"
        "Beta", "52WeekHigh", "52WeekLow",
        "50DayMovingAverage", "200DayMovingAverage"
    ]
    
    # Read the existing CSV file into a DataFrame
    df = pd.read_csv('./nyse_active_stocks/nyse_all_tickers_raw.csv')
    
    # Create an empty list to store the dictionaries of fundamental values
    fundamental_values_list = []

    # Create threads for each symbol
    threads = []
    for symbol in df['symbol']:
        time.sleep(0.2)
        thread = threading.Thread(target=get_fundamentals_for_symbol, args=(symbol, fundamentals, fundamental_values_list))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Convert the list of dictionaries into a DataFrame
    new_df = pd.DataFrame(fundamental_values_list)
    
    # Add 'symbol' column to the DataFrame
    new_df['symbol'] = df['symbol']
    
    # Concatenate the existing DataFrame with the new DataFrame
    final_df = pd.concat([df, new_df], axis=1)
    
    # Save the DataFrame to a new CSV file
    final_df.to_csv('./nyse_active_stocks/nyse_all_tickers_processed.csv', index=False)

# Call the function
# get_allinfo_for_ticker()


#drop all NA values from raw file above.
# df = pd.read_csv('./nyse_active_stocks/nyse_all_tickers_processed.csv')

# # Drop rows where specified columns have NaN values
# columns_to_check = ['52WeekHigh', '52WeekLow', '50DayMovingAverage', '200DayMovingAverage']
# df = df.dropna(subset=columns_to_check, how='all')

# # Save the modified DataFrame to a new CSV file
# df.to_csv('new_file.csv', index=False)

# print(df)

#Function to pull technical_indicators for all stocks in file new_file.csv



#helper function to get technical indicators 

#indicators exponential moving average (EMA) function=EMA
#volume weighted average price (VWAP) function=VWAP
# moving average convergence / divergence (MACD) function=MACD
#stochastic oscillator (STOCH) function=STOCH
# relative strength index (RSI) values.function=RSI
#average true range (ATR) function=ATR
# Bollinger bands (BBANDS) function=BBANDS


def get_technicals_for_symbol(symbol, technicals, technical_values_list):
    technicals_name_list = ["EMA","MACD","STOCH","RSI","ATR","BBANDS"]
    for technical_name in technicals_name_list:


        try:
           url =f"https://www.alphavantage.co/query?function={technical_name}&symbol={symbol}&interval=monthly&time_period=10&series_type=open&apikey=JEVABQILJD0BSD1C"

           print("url",url)
           r = requests.get(url)
           data = r.json()


			# Initialize a dictionary to store the fundamental values for this symbol
           technical_values = {'symbol': symbol}

		# Iterate over each fundamental
           for tech in technicals_name_list:
			# Try to retrieve the value for the fundamental
               new_value_tech = data.get(tech, 'NA')
               print("working to get data for all tickers", new_value_tech)

			# Store the value in the dictionary
               technical_values[tech] = new_value_tech

			# Append the dictionary to the list
               technical_values_list.append(technical_values)
        except Exception as e:
           print(f"Error occurred for symbol {symbol}: {e}")



def get_allinfo_for_ticker2():
    # Define the list of technicals indicators
    technicals_name_list = ["EMA","MACD","STOCH","RSI","ATR","BBANDS"]
   
    
    # Read the existing CSV file into a DataFrame
    df = pd.read_csv('new_file.csv') # new_file is a file that contains all values for fundamentals, it has 4520 values in all.
    print("df",df)
    # Create an empty list to store the dictionaries of fundamental values
    technical_values_list = []

    # Create threads for each symbol
    threads = []
    for symbol in df['symbol']:
        time.sleep(0.2)
        thread = threading.Thread(target=get_technicals_for_symbol, args=(symbol, technicals_name_list, technical_values_list))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Convert the list of dictionaries into a DataFrame
    new_df = pd.DataFrame(technical_values_list)
    
    # Add 'symbol' column to the DataFrame
    new_df['symbol'] = df['symbol']
    
    # Concatenate the existing DataFrame with the new DataFrame
    final_df = pd.concat([df, new_df], axis=1)
    
    # Save the DataFrame to a new CSV file
    final_df.to_csv('./nyse_active_stocks/nyse_final.csv', index=False)


# get_allinfo_for_ticker2()

technicals_name_list = ["EMA","MACD","STOCH","RSI","ATR","BBANDS"]


# for tech in technicals_name_list:
# 	try:

# 		url =f"https://www.alphavantage.co/query?function={tech}&symbol=A&interval=monthly&time_period=10&series_type=open&apikey=JEVABQILJD0BSD1C"
# 		print("url",url)
# 		r = requests.get(url)
# 		data = r.json()
# 		print("data",data)
# 		#print(data[f'Technical Analysis: {tech}']['2024-02-12'])
# 	except:
# 		pass

url =f"https://www.alphavantage.co/query?function=EMA&symbol=A&interval=monthly&time_period=10&series_type=open&apikey=JEVABQILJD0BSD1C"
print("url",url)
r = requests.get(url)
data = r.json()
print("data",data['Technical Analysis: EMA']['2024-01-31'])