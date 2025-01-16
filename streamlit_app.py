import streamlit as st
from openai import OpenAI
import json

# Show title and description.
st.title("💬 Get into the best MBA school")
st.write(
    "We are a team of 36 elite business school insiders, including former admissions directors from the top schools."
)
st.write(
    "Chat privately with our AI about your background and MBA goals, to work out who is best placed to help you."
)

if "answers" not in st.session_state: 
    #st.session_state.ai_response = None
    #st.session_state.original_text = ''
    st.session_state.answers = []

client = OpenAI(api_key=st.secrets["openai_key"])
def submit_enquiry():
    enquiry = f"I need help applying to MBA schools. My goals are: {goals}. My background: {background}."

    prompt = f"You are the receptionist at Fortuna Admissions, the dream team of fictional movie characters and former Admissions Directors from the world\'s top business schools, providing advisory services to help MBA applicants strengthen their profile, position their application and target the best schools. Respond to the following enquiry from an MBA applicant with 3 answers, each from a fictional movie character or Heidi Hillis a Fortuna Consultant, each giving an in-character response to the enquiry. For each response, introduce yourself, compliment the applicant on a particular aspect of their background or experience, and explain how your own experience is relevant to helping the applicant, then explain the help available, including essay editing and mock interviews, asking an insightful and deeply probing hypothetical question about the background of the applicant as an example of what might be asked for an essay or mock interview. Finally mention a date and time in {country} when the character is next available for a consultation, and ask for the applicant to provide contact details as a next step. Separate each response with the string <hr>. Here's the enquiry: {enquiry}."

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    response_dict = ai_response.model_dump()
    message_content = response_dict["choices"][0]["message"]["content"]

    st.session_state.answers = message_content.split('<hr>')


background = st.text_area('Tell us about yourself. Copy & paste some excerpts from your resume or LinkedIn profile, or write a brief summary. Your name and contact details are not required.')

if background:
    goals = st.text_area('Great! What are your MBA goals? Are there specific schools and programs that have captured your attention?')

    if goals:
        country = st.selectbox(
            'Fantastic! Final question: what\'s your country of residence?',
            ['', 'Australia', 'United States']
        )

        submit_button = st.button('Submit', type="primary", on_click=submit_enquiry, disabled=not country)

    else:
        goals_next = st.button('Next', type="primary")

else:
    background_next = st.button('Next', type="primary")

if False and st.session_state.ai_response:
    with st.chat_message("assistant"):
        #st.write_stream(st.session_state.ai_response)
        st.markdown(st.session_state.original_text)

    name = st.text_input('Name')
    email = st.text_input('Email')

if st.session_state.answers:
    st.markdown(
        """
        <style>
        .stColumn {
            padding: 10px;
            background-color: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 5px;
            height: 500px;
            overflow: scroll;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    cols = st.columns(len(st.session_state.answers))

    # Display each answer in its respective column
    for idx, (col, answer) in enumerate(zip(cols, st.session_state.answers)):

        with col:

            if 'Heidi Hillis' in answer:
                answer = answer.replace('Heidi Hillis', '<a href="https://fortunaadmissions.com/team-member/heidi-hillis/" target="_blank">Heidi Hillis</a>')
                st.html('<a href="https://fortunaadmissions.com/team-member/heidi-hillis/" target="_blank"><img src="https://fortunaadmissions.com/wp-content/uploads/2017/08/heidi-cropped.jpg" width="100%" /></a>')

            st.markdown(answer, unsafe_allow_html=True)

            name = st.text_input('Name', key=f'name-{idx}')
            email = st.text_input('Email', key=f'email-{idx}')
            enquiry_button = st.button('Submit', key=f'submit-{idx}', type="primary")

            if 'Heidi Hillis' in answer:
                st.html('<hr>')
                st.html('<b>Recent articles by Heidi</b>')
                st.html('<a href="https://fortunaadmissions.com/how-to-create-a-career-vision-for-your-mba-application/" target="_blank">How to Create a Career Vision For Your MBA Application</a>')
                st.html('<a href="https://fortunaadmissions.com/author/heidi/" target="_blank">More...</a>')
