from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm=HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-alpha",
    task="text-generation"
)

model=ChatHuggingFace(llm=llm)

results=model.invoke("What is the capital of India?")
print(results.content)