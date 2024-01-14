import streamlit as st
from bi_assistant import BIAssistant
import config

# Initialize the BIAssistant
assistant = BIAssistant(api_key= config.API_KEY, database_uri= config.DATABASE_URI)

# Title of the web app
st.title('IMDB - BI Assistant')

# Text input for the user's question
user_question = st.text_input("Enter your question about the IMDB dataset:")

# Button for submitting the question
if st.button('Submit'):
    with st.spinner('Processing...'):
        # Call the method to answer the question
        answer = assistant.question_answering_imdb(user_question)
        # Display the answer
        st.write(answer)