import streamlit as st
import google.generativeai as gemini

st.set_page_config(page_title="conversationai", page_icon="🤖", layout="wide")

title_style = {"color": "darkblue", "font-size": "40px", "font-weight": "bold", "text-align": "center", "padding": "20px"}

subtitle_style = {"color": "darkorange", "font-size": "28px", "font-weight": "bold", "text-align": "center", "padding": "10px"}

st.markdown('<p style="{}"> 🤖 AI Data Science Tutor </p>'.format(";".join([f"{k}:{v}" for k, v in title_style.items()])), unsafe_allow_html=True)


f = open(r"C:\Users\hp\Desktop\Data Science\Internship_innomatics_2024\Gemni\data\.gemni.txt")
api_key = f.read()

gemini.configure(api_key=api_key)
model = gemini.GenerativeModel(model_name="gemini-1.5-pro-latest",
                               system_instruction="""You are AI Assistant to resolve data science
                               Queries of the user.""")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, this is Gemini and how I can help you today?"}
    ]
    st.title("📢:rainbow[Howdy, How may I help you today?]")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input()

if user_input is not None:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            ai_response = model.generate_content(user_input)
            st.write(ai_response.text)
    new_ai_message = {"role": "assistant", "content": ai_response.text}
    st.session_state.messages.append(new_ai_message)
