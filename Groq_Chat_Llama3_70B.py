import streamlit as st
from groq import Groq
import os

st.title('Chat with Groq - Llama 3 70B')

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

if 'messages' not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    system_prompt = st.text_area('System Prompt', value='You are a helpful assistant.')
    temperature = st.slider('Temperature', 0.00, 2.00, 0.75, step=0.01)
    max_tokens = st.slider('Max Tokens', 0, 8192, 8192, step=1)
    top_p = st.slider('Top P', 0.00, 1.00, 1.00, step=0.01)

    if st.button('New Chat'):
        st.session_state.messages = []
        st.experimental_rerun()

user_input = st.chat_input('Say something...')

if user_input:
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    messages = [{'role': 'system', 'content': system_prompt}] + st.session_state.messages

    chat_completion = client.chat.completions.create(
        messages=messages,
        model='llama3-70b-8192',
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stop=None,
        stream=False
    )

    response = chat_completion.choices[0].message.content
    st.session_state.messages.append({'role': 'assistant', 'content': response})

    for msg in st.session_state.messages:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'], unsafe_allow_html=True)
