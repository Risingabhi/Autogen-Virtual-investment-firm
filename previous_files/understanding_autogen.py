
import autogen
from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent #function calling
import os
import openai
import yfinance as yf #to pull current market data 





client = openai.OpenAI()

os.environ["OPENAI_API_KEY"] = "Your OPENAI_API_KEY"  #ULRICH API

config_list = [
    {
        'model': 'gpt-3.5-turbo',
    }
    ]


gpt4_config = {"config_list": config_list, "temperature":0, "seed": 53}




def get_stock_price(symbol:str)-> float:
    stock = yf.Ticker(symbol)
    price = stock.history(period ="1d")['close'].iloc[-1]
    return price 


#critical for function calls.
tools_list = [{
    "type": "function",
    "function": {
        "name": "get_stock_price",
        "description": "Retrieve the latest closing price of a stock using its ticker symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The ticker symbol of the stock"
                }
            },
            "required": ["symbol"]
        }
    }
}]

llm_config = {
    "tools" : tools_list
}

# investment_analyst = autogen.AssistantAgent(name="investment_analyst",llm_config={
#                                                                   "config_list": config_list,
#                                                                 "temperature": 0.5},
#                 system_message ="""You are investment analyst who recommends best stocks considering global leading stock exchanges by using yfinance and alpha vantage api,
#                 api key for alphavantage is KFGE5HXRO7G42KVK.""",
#                 description ="This agent is responsible for recommending best stocks",


                                
                                
# )
                               
investment_analyst = GPTAssistantAgent(name="investment_analyst",
                                instructions =""""
    You are a Stock Expert. 
    Reply TERMINATE when the task is solved and there is no problem
    """,
                llm_config = llm_config,


                                
                                
)


investment_analyst.register_function(
    function_map={
        "get_stock_price": get_stock_price,
    }
)                               
                               




user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False, 
        },
     #Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    system_message ="""you are a HUMAN ADMIN and can execute python code , reply once done.Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""

)


# groupchat = autogen.GroupChat(agents=[user_proxy,investment_analyst], messages=[], max_round=20)
# manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=gpt4_config)
#user_proxy.initiate_chat(investment_analyst, message="plot YOY movement of NYSE for 2 years ")
user_proxy.initiate_chat(investment_analyst, message="plot movement of ACC in BSE for 31st Dec 2023")