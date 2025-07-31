from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import requests

load_dotenv()

model=ChatGoogleGenerativeAI(model='gemini-2.5-pro')

search=DuckDuckGoSearchRun()

@tool
def weather(city: str) -> str:
    '''Get current weather of the given city'''
    url=f"http://api.weatherstack.com/current?access_key=c8433176a321066bf5927cbd23df2e47&query={city}"
    response=requests.get(url)
    return response.json()

prompt=hub.pull("hwchase17/react")


agent= create_react_agent(
    llm=model,
    tools=[search,weather],  
    prompt=prompt
)

agent_executer=AgentExecutor(
    agent=agent,
    tools=[search,weather],
    verbose= True
)

response=agent_executer.invoke({"input":"What is the temperature and humidity of biggest city in Madhya Pradesh"})
print(response)
print(response['output'])