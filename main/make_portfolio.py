# main file for investment_analyst work.
# read relevant excel files and pull data.
#leverage CAPM to know returns for each stock, 
#find risk values for each stock by looking at beta values.

#finally make three segments of stocks [high returns> 15%, medium return 8-10%, low returns < 8%] save these stocks in three files 

#high Return, medium return and low return.



'''takes 2 files as input 
for risk calculation - we need historical data - saved in ./previous_files/symbol_data.csv

for return calculation we need 
~ 1.Beta of stock, 
~2 . Rm- Return of the market S&P(500), for 10 years
~ 3. Rf Govt bond yield current.'''

import requests
import json 
import pandas as pd 

#https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey=demo
govt_yield_url =  f"https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey=JEVABQILJD0BSD1C"
r = requests.get(govt_yield_url)
Risk_free_govt_yield = r.json()
latest_rate = (Risk_free_govt_yield['data'][0])['value']




# SandP_rate_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={symbol}&apikey=JEVABQILJD0BSD1C"
# s = requests.get(SandP_rate_url)
expected_SandP_rate = 10.26


def cal_expected_return(latest_rate,expected_SandP_rate):
	#Expected_return_stock = Risk_free_govt_yield + beta*(Expected_S&P_return - Risk_free_govt_yield)

	df = pd.read_csv('alpha_beta_data.csv')
	  # Calculate and store the Expected_return_stock values
	expected_return_stocks = []
	# Iterate over the rows of the DataFrame
	for index, row in df.iterrows():
		symbol = row['Symbol']
		alpha = row['Alpha']
		beta = row['Beta']
		
	
	
		Expected_return_stock = (float(latest_rate)) + float(beta)*(float(expected_SandP_rate)) - (float(latest_rate))
		expected_return_stocks.append(Expected_return_stock)
		 # Add a new column to the DataFrame for Expected_return_stock
	df['Expected_return_stock'] = expected_return_stocks

	    # Write the updated DataFrame back to the Excel file
	df.to_csv('alpha_beta_data_with_expected_return.csv', index=False)

	    # Print a message
	print("Expected return values written to 'alpha_beta_data_with_expected_return.xlsx'")





# cal_expected_return(latest_rate,expected_SandP_rate)

def cal_risk():
	# Load the data
	df = pd.read_csv('symbol_data.csv')

	# Convert the Date column to datetime
	df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

	# Calculate daily returns
	df['Daily_Return'] = df.groupby('Symbol')['Close'].pct_change()

	# Calculate standard deviation of daily returns for each stock
	risk_data = df.groupby('Symbol')['Daily_Return'].std()

	# Calculate the average price for each stock
	average_price = df.groupby('Symbol')['Close'].mean()

	# Calculate the risk percentage
	risk_data_percent = (risk_data / average_price) * 100

	df2 = pd.read_csv('alpha_beta_data_with_expected_return.csv')

	# Add the risk percentage column to the DataFrame
	df2['Risk_Percentage'] = df2['Symbol'].map(risk_data_percent)

	# Save the DataFrame back to the CSV file
	df2.to_csv('risk_return_final.csv', index=False)

	# Display the result
	print(risk_data_percent)



# understand return expected in case not clear , lets say 10%. 
#calculate 10% of total investments = R
#make an optimization model

# R = return_from_stock1 + return_from_stock2 

#return_from_stock1 = amount invested in stock1 * Expected Return from Stock 1 
def making_portfolio_strategy():
	df1 = pd.read_csv('alpha_beta_data_with_expected_return.csv')
	print(df1)
	df2 = pd.read_csv('symbol_data.csv')
	print(df2)
	return df1,df2