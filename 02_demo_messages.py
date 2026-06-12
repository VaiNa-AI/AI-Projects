from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")

COMPANY = "TechShop"                       # change it → persona changes
conversation = [SystemMessage(content=(
    f"You are a customer support agent for {COMPANY}, "
    "an electronics store. Be concise. 2-3 sentences max."))]

def chat_turn(user_input):
    conversation.append(HumanMessage(content=user_input))
    response = llm.invoke(conversation)
    conversation.append(response)          # memory lives HERE — you own it
    print(f"Agent: {response.content}")

chat_turn("What is your return policy?")
chat_turn("How long do I have to return something?")
chat_turn("I bought a laptop 25 days ago. Can I still return it?")