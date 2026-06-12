from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
load_dotenv()

def get_time(city: str) -> str:
    """
    Get the current time for a given city
    Use this when the user asks about current time or local time.
    
    Args:
        city: the name of the city (e.g. 'Delhi', 'London', 'New York', 'Paris')
    Returns:
        The current time for the given city
    """
def get_date(city: str) -> str:
    """
    Get the current date for a given city
    Use this when the user asks about current date.
    
    Args:
        city: the name of the city (e.g. 'Delhi', 'London', 'New York', 'Paris')
    Returns:
        The current date for the given city
    """

    time_data = {
        'paris': '10am',
        'delhi': '11am',
        'london': '12pm',
        'new york': '10pm'
    }

    date_data = {
        'paris': 'Jun 6th',
        'delhi': 'Jun 6th',
        'london': 'Jun 6th',
        'new york': 'Jun 6th'
    }
    time = time_data.get(city.lower(), 'unknown')
    return f"The time in {city} is {time}"

    date = date_data.get(city.lower(), 'unknown')
    return f"The time in {city} is {date}"

agent = create_agent(
    model="gpt-5.4-mini",
    tools=[get_time, get_date],
    system_prompt="You are a helpful assistant",
)
r1 = agent.invoke({"messages": [{"role": "user",
              "content": "what is the time in delhi"}]}) # documentation approach
print(r1)
print("--------------------------------")
r2 = agent.invoke({"messages": [HumanMessage(content="what is the time in delhi")]}) # direct approach
print(r2)
print("--------------------------------")
r3 = agent.invoke({"messages": [HumanMessage(content="what is the date in delhi")]}) # direct approach
print(r3)
print("--------------------------------")