import autogen
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent
import openai
import yfinance as yf
import os
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
import asyncio

# #to check panel 
import panel as pn

from panel.template import DarkTheme

template = pn.template.MaterialTemplate(title='Material Dark', theme=DarkTheme)

import os
openai_api_key = os.getenv("YOUR_OPENAI_API_KEY")

# os.environ["OPENAI_API_KEY"] = ""

client = openai.OpenAI()

input_future = None

def get_stock_price(symbol: str) -> float:
    stock = yf.Ticker(symbol)
    price = stock.history(period="1d")['Close'].iloc[-1]
    print(f'price of your stock is {price}')


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


# Example usage
index_symbol = "^GSPC"  # S&P 500 in
tools_list = [{
    "type": "function",
    "function": {
        "name": "plot_monthly_index_movement",
        "description": "get monthly index movement for a given period.",
        "parameters": {
            "type": "object",
            "properties": {
                "index_symbol": {
                    "type": "string",
                    "description": " symbol of index"
                },
                "start_date": {
                    "type": "string",
                    "description": " start date for calculating index movement"
                },
                "end_date": {
                    "type": "string",
                    "description": " end date for calculating index movement"
                }
            },
            "required": ["index_symbol", "start_date", "end_date"]
        }
    }
},
# {
#     "type": "function",
#     "function": {
#         "name": "get_stock_price",
#         "description": "get stock price.",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "symbol": {
#                     "type": "string",
#                     "description": "get stock price basis symbol"
#                 }
#             },
#             "required": ["name of stock"]
#         }
#     }
# }]
]
llm_config = { 
    "tools": tools_list,
}


gpt_assistant = GPTAssistantAgent(
    name="investment Analyst",
    instructions="""
    You are a investment Analyst.
    Reply TERMINATE when the task is solved and there is no problem
    """,
    llm_config=llm_config
)
gpt_assistant.register_function(
    function_map={
        "plot_monthly_index_movement": plot_monthly_index_movement,
        
    }
)

user_proxy = autogen.UserProxyAgent(
    name="mervinpraison",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir" : "coding",
    }
)


ceo = GPTAssistantAgent(
    name="ceo",
    instructions="""
    You are a ceo, and will direct gpt assistant to do the task, 
    Reply TERMINATE when the task is solved and there is no problem
    """,
    llm_config=llm_config
)
# user_proxy.initiate_chat(
#     gpt_assistant,
#     message="""
#     plot index movement'^GSPC' from 2023-10-01 till 2023-11-01 , also find stock price of Apple.
#     """
# )


# def print_messages(recipient, messages, sender, config):

#     #chat_interface.send(messages[-1]['content'], user=messages[-1]['name'], avatar=avatar[messages[-1]['name']], respond=False)
#     print(f"Messages from: {sender.name} sent to: {recipient.name} | num messages: {len(messages)} | message: {messages[-1]}")
    
#     if all(key in messages[-1] for key in ['name']):
#         chat_interface.send(messages[-1]['content'], user=messages[-1]['name'], avatar=avatar[messages[-1]['name']], respond=False)
#     else:
#         chat_interface.send(messages[-1]['content'], user='SecretGuy', avatar='🥷', respond=False)
    
#     return False, None  # required to ensure the agent communication flow continues


def print_messages(recipient, messages, sender, config):
    output_file = "output.txt"

    # Extract the relevant message content and sender/recipient names
    sender_name = sender.name
    recipient_name = recipient.name
    last_message = messages[-1]['content']

    print(f"Messages from: {sender_name} sent to: {recipient_name} | num messages: {len(messages)} | message: {last_message}")

    try:
        # Append the message to the output file
        with open(output_file, "a", encoding='utf-8') as f:
            f.write(f"Sender: {sender_name}\nRecipient: {recipient_name}\nMessage: {last_message}\n\n")
    except Exception as e:
        print(f"Error: {e}")

    if 'name' in messages[-1]:
        chat_interface.send(last_message, user=sender_name, avatar=avatar.get(sender_name, 'DefaultAvatar'), respond=False)
    else:
        chat_interface.send(last_message, user='SecretGuy', avatar='🥷', respond=False)

    return False, None  # Required to ensure the agent communication flow continues


initiate_chat_task_created = False




avatar = {user_proxy.name:"👩‍💻",gpt_assistant.name:"📝",ceo.name:"📝"}

async def delayed_initiate_chat(agent, recipient, message):

    global initiate_chat_task_created
    # Indicate that the task has been created
    initiate_chat_task_created = True

    # Wait for 2 seconds
    await asyncio.sleep(2)

    # Now initiate the chat
    await agent.a_initiate_chat(recipient, message=message)

async def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    
    global initiate_chat_task_created
    global input_future

    if not initiate_chat_task_created:
        asyncio.create_task(delayed_initiate_chat(ceo, manager, contents))
        # asyncio.create_task(interviewer_speech(manager))

    else:
        if input_future and not input_future.done():
            input_future.set_result(contents)
        else:
            print("There is currently no input being awaited.")



#register reply to be shown in chat.

chat_interface = pn.chat.ChatInterface(callback=callback )
user_proxy.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)
gpt_assistant.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)
ceo.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)







groupchat = autogen.GroupChat(agents=[user_proxy,ceo,gpt_assistant], messages=[], max_round=10)
manager = autogen.GroupChatManager(groupchat=groupchat)
chat_interface.send("Welcome to Phoenix Investments LLC, an Ai Company that returns best returns, provide your financial objectives", user="System", respond=False)




#chat_interface.servable()
# user_proxy.initiate_chat(gpt_assistant,message=" find index movement for ^GSPC from 2023.10.01 to 2023.12.01")