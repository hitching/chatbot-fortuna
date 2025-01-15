import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Fortuna Admissions AI Chat")
st.write(
    "Chat privately with our AI about your background and MBA goals, and how Fortuna can help."
)

if "ai_response" not in st.session_state: 
    st.session_state.ai_response = None

client = OpenAI(api_key=st.secrets["openai_key"])
def submit_enquiry():
    enquiry = f"I need help applying to MBA schools. My goals are: {goals}. My background: {background}."
    prompt = f"You are the receptionist at Fortuna Admissions, the dream team of fictional movie characters and former Admissions Directors from the world\'s top business schools, providing advisory services to help MBA applicants strengthen their profile, position their application and target the best schools. Respond to the following enquiry from an MBA applicant with 3 answers, each from a fictional movie character or Heidi Hillis a Fortuna Consultant, each giving an in-character response to the enquiry. For each response, introduce yourself, compliment the applicant on a particular aspect of their background or experience, and explain how your own experience is relevant to helping the applicant, then explain the help available, including essay editing and mock interviews, asking an insightful and deeply probing hypothetical question about the background of the applicant as an example of what might be asked for an essay or mock interview. Finally mention a date and time when the character is next available for a consultation, and ask for the applicant to provide contact details as a next step. Here's the enquiry: {enquiry}."

    st.session_state.ai_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        stream=True,
    )

background = st.text_area('Tell us about your background. Paste in your resume, or parts of your LinkedIn profile, or write a brief summary. Your name and contact details are not required.')

if background:
    goals = st.text_area('What are your MBA goals? Which schools and programs are you interested in applying for?')

    if goals:
        country = st.selectbox(
            'And finally, what\'s your country of residence?',
            ['', 'Australia', 'United States']
        )

        submit_button = st.button('Submit', type="primary", on_click=submit_enquiry, disabled=not country)

if st.session_state.ai_response:
    with st.chat_message("assistant"):
        st.write_stream(st.session_state.ai_response)