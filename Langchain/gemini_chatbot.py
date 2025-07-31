from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

model = ChatGoogleGenerativeAI(
    model='gemini-2.5-pro',
    temperature=0.7,
    top_p=0.8,
    top_k=10
    # max_output_token=500
)

messages = [
    SystemMessage(content='You are an AI chatbot which gives answers in a friendly way.')
]

while True:
    user_input = input('You: ')
    if user_input.lower() in ['exit', 'quit']:
        break

    messages.append(HumanMessage(content=user_input))

    response = model.invoke(messages)

    print('AI:', response.content)

    messages.append(AIMessage(content=response.content))
