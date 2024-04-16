import streamlit as st
from openai import OpenAI


f = open('keys/.openai_api_key.txt')
OPENAI_API_KEY = f.read()

client = OpenAI(api_key = OPENAI_API_KEY)

st.title("Code Correction using AI")



prompt = st.text_area("Enter your code...", height=10)

def chat_openai(prompt):

    st.balloons()
    response = client.chat.completions.create(
                      model="gpt-3.5-turbo-16k-0613",
                      messages=[
                          {"role": "system", "content": """You are a teaching assistant for students. you need to explain student where they done mistakes and fix the bugs"""},
                          {"role": "user", "content": prompt}
                      ]
                )
    return response.choices[0].message.content
if st.button("Fix Code"):

    st.write(chat_openai(prompt))
