from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm1=HuggingFaceEndpoint(repo_id='tiiuae/falcon-7b-instruct',task='text-generation')
model1=ChatHuggingFace(llm=llm1)

llm2=HuggingFaceEndpoint(repo_id='iarfmoose/t5-base-question-generator',task='text2text-generation')
model2=ChatHuggingFace(llm=llm2)

prompt1=PromptTemplate(
    template='Give me the detailed notes on topic {topic}',
    input_variables=['topic']
)

prompt2=PromptTemplate(
    template='Give me the 5 question quiz on the notes given {text}',
    input_variables=['text']
)

parser= StrOutputParser()

chain= prompt1 | llm1 | prompt2 | llm2 | parser

result= chain.invoke({'topic': 'Python in machine learning'})

print(result)

