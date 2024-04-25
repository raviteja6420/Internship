from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_core.prompts import ChatPromptTemplate,HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
import streamlit as st 
import nltk
nltk.download('punkt')

# Title for the Streamlit application
st.title(":robot_face: :rainbow[Retrieval Augmented Generation System for Q & A Chat Bot]")
st.markdown(":rainbow[You can ask me anything from :orange['Leave No Context Behind'] Paper]")

# Gemini-api-key
f = open('data/.api_key_dp.txt')
api_key = f.read()

# Creating chat model
chat_model = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-1.5-pro-latest")

# Creating embedding model
embedding_model = GoogleGenerativeAIEmbeddings(google_api_key=api_key, model="models/embedding-001")

# Set up a connection with the Chroma
connection = Chroma(persist_directory="data/Chroma_db_for_rag", embedding_function=embedding_model)


retriever = connection.as_retriever(search_kwargs={"k": 5})

# query
user_query = st.text_input(":blue[Please Enter your query...]")

# Chatbot prompt templates
chat_template = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a Helpful AI Bot. You take the context and question from user. Your answer should be based on the specific context."),
    HumanMessagePromptTemplate.from_template("Answer the question based on the given context.\nContext: {Context}\nQuestion: {question}\nAnswer:")
])

# Output parser for chatbot response
output_parser = StrOutputParser()

# Function to format retrieved documents
def format_docs(docs):
    formatted_content = "\n\n".join(doc.page_content.strip() for doc in docs if doc.page_content.strip())
    return formatted_content if formatted_content else "No relevant context found."

# RAG chain for chatbot interaction
rag_chain = (
    {"Context": retriever | format_docs, "question": RunnablePassthrough()}
    | chat_template
    | chat_model
    | output_parser
)

if st.button("Result"):
    if user_query:
        response = rag_chain.invoke(user_query)
        st.write(response)