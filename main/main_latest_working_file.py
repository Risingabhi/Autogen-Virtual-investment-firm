import autogen
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
import openai
import yfinance as yf
import os
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
# import panel as pn
import time
import asyncio
from datetime import datetime, timedelta
from make_portfolio import *

# from panel.template import DarkTheme

# template = pn.template.MaterialTemplate(title='Material Dark', theme=DarkTheme)
import os
openai_api_key = os.getenv("OPENAI_API_KEY")



client = openai.OpenAI()


input_future = None

class MyConversableAgent(autogen.ConversableAgent):

    async def a_get_human_input(self, prompt: str) -> str:
        global input_future
        print('AGET!!!!!!')  # or however you wish to display the prompt
        chat_interface.send(prompt, user="System", respond=False)
        # Create a new Future object for this input operation if none exists
        if input_future is None or input_future.done():
            input_future = asyncio.Future()

        # Wait for the callback to set a result on the future
        await input_future

        # Once the result is set, extract the value and reset the future for the next input operation
        input_value = input_future.result()
        input_future = None
        return input_value



# =========================================================ALL FUNCTIONS TO BE USED IN CODE =================


def calculate_dates():
    # Calculate start_date (1 year earlier from today)
    end_date = datetime.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=365)
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')


def get_stock_price(symbol: str) -> float:
    stock = yf.Ticker(symbol)
    price = stock.history(period="1d")['Close'].iloc[-1]
    print(f'price of your stock is {price}')




# using top few stock exchanges to reduce load 

def get_monthly_index_movement():
    index_symbols = ["^NYA", "^NDX", "^SSE", "^IXIC", "^BSESN", "^MXX"]
    start_date, end_date = calculate_dates()
    
    start_date = datetime.now() - timedelta(days=365)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = datetime.now() - timedelta(days=1)
    end_date = end_date.strftime('%Y-%m-%d')
    print("start_date",start_date)
    print("end_date",end_date)
    # Create an empty dataframe to store the data for all stock exchanges
    all_data = pd.DataFrame()

    for index_symbol in index_symbols:
        # Fetch the historical data for the index
        print("INDEX",index_symbol)
        index_data = yf.download(index_symbol, start=start_date, end=end_date)

        # Check if the data is empty
        if index_data.empty:
            print(f"{index_symbol}: No price data found, symbol may be delisted or incorrect (1d {start_date} -> {end_date})")
            continue

        # Resample the data to get the last price of each month
        monthly_data = index_data.resample('ME').last()

        # Calculate monthly movements
        monthly_data['Monthly Movement'] = monthly_data['Close'].pct_change() * 100

        # Insert the index symbol as the first column
        monthly_data.insert(0, 'Index Symbol', index_symbol)

        # Append the data to the all_data dataframe
        all_data = pd.concat([all_data, monthly_data])

    # Ensure the directory exists
    directory = "index_data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the CSV file path for all data
    csv_file_path = os.path.join(directory, f"all_index_data_{start_date}_to_{end_date}.csv")

    # Save all the monthly data to a single CSV file
    all_data.to_csv(csv_file_path, index=False)  # Set index=False to exclude the DataFrame index
    print(f"All data saved to {csv_file_path}")





#Keeping this fixed path 

def read_text_file():
    file_path = "C:/Users/Risin/Desktop/my_poc/Ulrich_Autogen_investment/coding/financial_report.txt"
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            print(file_content)
    except FileNotFoundError:
        return f"File '{file_path}' not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def save_text_to_file(text):
    with open('my_portfolio.txt', 'w') as file:
        file.write(text)
# Example usage
# index_symbol = "^GSPC"  # S&P 500 in
tools_list = [{
    "type": "function",
    "function": {
        "name": "get_monthly_index_movement",
        "description": "get the monthly index movement",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "get the monthly index movement"
                }
            },
            "required": ["get the monthly index movement"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_stock_price",
        "description": "get stock price.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "get stock price basis symbol"
                }
            },
            "required": ["symbol"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "read_text_file",
        "description": "read content of file",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "contents of the file "
                }
            },
            "required": ["content"]
        }

    }

},
{
    "type": "function",
    "function": {
        "name": "making_portfolio_strategy",
        "description": "read content of csv",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "contents of the file "
                }
            },
            "required": ["contents of the file"]
        }

    }

},
{
    "type": "function",
    "function": {
        "name": "save_text_to_file",
        "description": "write text to file",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "summary"
                }
            },
            "required": ["summary"]
        }

    }

}]





# ====:::::::::::::::::::::::::::::::::::::::::::::::::::::CONFIGS
llm_config = { 
    "tools": tools_list,
    "config_list": [
            {
                "model": "gpt-4o-mini"
                }]
            }
                # other parameters
            



#models gpt-4-turbo-preview
#model earlier =gpt-4-1106-preview
config_list = [
    {
        'model': 'gpt-4o-mini',
    }
    ]

gpt4_config = {"config_list": config_list, "temperature":0, "seed": 53}
# =================================================================ALL AGENTS :::::::::::::::::::::::::::::::::::::::::::::::



# ==========================================================================ALL AGENTS 
# 1-this agent represents the actual candidate,
user = MyConversableAgent(
name="user",
human_input_mode="ALWAYS",
max_consecutive_auto_reply=10,
system_message = """ You will provide investment amount,,time_horizon and budget to ceo and ceo should delegate this to investment_analyst.""",
is_termination_msg=lambda x:x.get("content", "").rstrip().endswith("TERMINATE"),
)

# 2- User proxy Agent with power to execute code 

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    code_execution_config={
        "work_dir" : "coding",
    }
)


# #2 Investment_Analyst & his assistant.
# 2- read text file with name financial_report.txt
#     3- get the monthly index movement for all listed exchange using index_symbols = ["^NYA", "^NDX", "^SSE", "^IXIC", "^BSESN", "^MXX"]


# we would diversify the portfolio across many stocks that meet the criteria, 
# and dynamic adjustments would be made based on the total expected return of the selected portfolio,
#  each stock's weight in the portfolio, and the associated risks.
# #exact allocation would also consider the risk tolerance of the investor, 
# correlation of the stock with the overall market, 
# and a diversification strategy to reduce the unsystematic risk.
#client is looking to invest $130,000 in stocks, expects a return of 7%, time horizon is 10 years. suggest a portfolio.
investment_analyst = GPTAssistantAgent(
    name="investment_analyst",
    instructions="""
    You are a investment_analyst, Your Standard Tasks are mentioned below.Remember you are expert and understand the process of designing portfolio for investors.
    you have access to a database management system and the necessary skills to update database, read database, delete database. 
    You also have professional knowledge and access to financial models and analysis tools.
    you will extract data using function making_portfolio_strategy –data will provide you risk and return for each stock and Open,High,Low,Close,Adjusted Close,Volume,Dividend Amount.Remember you'd use ONLY the data extracted to make portfolio.
    you will extract content by using function read_text_file and use that information to make your summary later
   
    you will do following tasks one by one to make a portfolio.

    Your Standard Tasks:
    1. calculate expected return on amount given by client by using suitable mathematical calculation.share your result. Be Brief.
    2.you will calculate amount to be invested in each selected stock [ALWAYS USE Close data of relevant stock extracted using making_portfolio_strategy, to make all calculations.], again by performing mathematical calculation, share final answer ONLY. Don’t share calculations.
    3. diversify the portfolio across many stocks that meet the criteria,ideally number of stocks selected should be atleast 20.Share selected stock list.
    4. Summary should contain ALL 20 stocks  selected. you will provide following details:
    sample summary for each stock would look like this:
    Name of stock  AA, Buy price $24.56 [use Close Price instead of Buy Price], Number of shares to be bought 100, expected return 15.65%, total amount invested in stock $2456, percent of funds allocated 10%
    Remember total_invested_amount = invested_amount_stock1, invested_amount_stock2 .... 
    5.After you made summary for all selected stocks, run function save_text_to_file and YOU MUST SAVE THE SUMMARY for all stocks and confirm the completion.Ensure you have entered details for all 20 stocks.


   

        Reply with "TERMINATE" once the task is completed and there are no issues.
            
    """,
    llm_config=llm_config
)
investment_analyst.register_function(
    function_map={
       
        
        "read_text_file": read_text_file,
        "making_portfolio_strategy": making_portfolio_strategy,
        "save_text_to_file":save_text_to_file,
    }
)

#3 CEO 


ceo = GPTAssistantAgent(
    name="ceo",
    
    instructions="""
    You are a ceo , welcome user and ask for investment objective with investment amount, time frame and expected return, pass this information to investment_analyst and instruct to make a portfolio by doing Standard Tasks.
    Reply TERMINATE when the task is solved and there is no problem
    """,
    llm_config=llm_config
)

#4 Portfolio_Manager
portfolio_manager = GPTAssistantAgent(
    name="portfolio_manager",
    
    instructions="""
    You are a portfolio manager, 
    Reply TERMINATE when the task is solved and there is no problem
    """,
    llm_config=llm_config
)

#5 
operations_manager = GPTAssistantAgent(
    name="operations_manager",
    
    instructions="""
    You are a operations manager 
    Reply TERMINATE when the task is solved and there is no problem
    """,
    llm_config=llm_config
)



# def print_messages(recipient, messages, sender, config):

#     #chat_interface.send(messages[-1]['content'], user=messages[-1]['name'], avatar=avatar[messages[-1]['name']], respond=False)
#     print(f"Messages from: {sender.name} sent to: {recipient.name} | num messages: {len(messages)} | message: {messages[-1]}")
    
#     if all(key in messages[-1] for key in ['name']):
#         chat_interface.send(messages[-1]['content'], user=messages[-1]['name'], avatar=avatar[messages[-1]['name']], respond=False)
#     else:
#         chat_interface.send(messages[-1]['content'], user='SecretGuy', avatar='🥷', respond=False)
    
#     return False, None  # required to ensure the agent communication flow continues





initiate_chat_task_created = False


groupchat = autogen.GroupChat(agents=[user,user_proxy,ceo,investment_analyst, portfolio_manager,operations_manager], messages=[], max_round=10)
manager = autogen.GroupChatManager(groupchat=groupchat)






# Save the conversation to a file
output_file = "agents_conversation.txt"

try:
    with open(output_file, "w", encoding='utf-8') as f:
        for message in groupchat.messages:
            # Write a separator
            f.write("-" * 20 + "\n")
            f.write(f'### {message["name"]} ###\n')
            f.write(message["content"] + "\n")
            f.write("-" * 20 + "\n")
except Exception as e:
    print(f"Error: {e}")
else:
    print(f"Conversation saved to {output_file}")


# best prompt tested 24.2.24
# ask investment_analyst to do standard task. This prompt makes investment analyst read financial_report and also runs monthly index movement.
user_proxy.initiate_chat(
    manager,
    message="""
    Allow ceo to welcome and collect information from user.
    """
)


''' You are a investment_analyst, Your Standard Tasks are mentioned below.Remember you are expert and understand the process of designing portfolio for investors.
    you have access to a database management system and the necessary skills to update database, read database, delete database. 
    You also have professional knowledge and access to financial models and analysis tools.
    you will extract data using function making_portfolio_strategy and also the risk and return for each stock, you will also extract Open,High,Low,Close,Adjusted Close,Volume,Dividend Amount.Remember you'd use this data ONLY to make portfolio.
    you will extract content by using function read_text_file and use that information to make your summary later.Enure your summary follows the format mentioned.
    share results of `making_portfolio_strategy` and `read_text_file` functions with all agents.
    you will do following tasks one by one to make a portfolio.

    Your Standard Tasks:
    1. calculate expected return on amount given by client by using suitable mathematical calculation.share result.Be Brief.
    2. once you know expected return , you will perform calculations basis Open,High,Low,Close,Adjusted Close,Volume,Dividend Amount, risk and return extracted earlier.
    No need to use get_stock_price function.USE Close price as Buy price to make all calculations.
    3.you will calculate amount to be invested in each selected stock basis Close, again by performing mathematical calculation, share final answer ONLY. Dont share calculations.
    4. diversify the portfolio across many stocks that meet the criteria,ideally number of stocks selected should be atleast 20.Share selected stock list.
    5. in your summary ensure you mention details for ALL 20 stocks  selected. you will provide following details:
    Name of stock, Buy price, Number of shares to be bought, expected return, total amount invested in stock.
    Remember total_invested_amount = invested_amount_stock1, invested_amount_stock2 .... 
    6.After you made summary run function save_text_to_file and insert summary made above and confirm the completion.

    
    Reply TERMINATE when the task is solved and there is no problem
ChatGPT
Here's a revised version of your prompt that is clearer and more structured:

You are an investment analyst with expertise in designing investment portfolios. Your role involves the following tasks:

Data Extraction: Use the making_portfolio_strategy function to extract the risk and return for each stock, as well as the Open, High, Low, Close, Adjusted Close, Volume, and Dividend Amount data. This data will be used exclusively for portfolio creation.

Information Gathering: Use the read_text_file function to extract content for later use in your summary. Ensure that your summary follows the specified format.

Result Sharing: Share the results of the making_portfolio_strategy and read_text_file functions with all agents.

Portfolio Creation: Perform the following steps to create a portfolio:

a. Expected Return Calculation: Calculate the expected return on the amount given by the client using appropriate mathematical calculations. Share the result briefly.

b. Stock Selection: Based on the expected return, perform calculations using the Open, High, Low, Close, Adjusted Close, Volume, Dividend Amount, risk, and return data extracted earlier. Use the Close price as the Buy price for all calculations.

c. Investment Allocation: Calculate the amount to be invested in each selected stock based on the Close price by performing mathematical calculations. Share the final answer only without the calculations.

d. Diversification: Diversify the portfolio across at least 20 stocks that meet the criteria. Share the list of selected stocks.

e. Summary Creation: In your summary, provide the following details for all 20 selected stocks: Name of the stock, Buy price, Number of shares to be bought, Expected return, Total amount invested in each stock. Ensure that the total invested amount is the sum of the amounts invested in each stock.

Summary Saving: After creating the summary, run the save_text_to_file function to save the summary and confirm the completion of the task.

Reply with "TERMINATE" once the task is completed and there are no issues.

'''