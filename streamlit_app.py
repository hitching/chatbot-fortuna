import streamlit as st
from openai import OpenAI

version = ''
if st.query_params.get("version") == 'heidi':
    version = 'or Heidi Hillis a Fortuna Consultant'

# Show title and description.
st.title("💬 Get into the best MBA school")
st.write("We are a diverse group of 36 elite business school insiders, including former admissions directors from the world's top schools, each offering unique expertise and insights, and together offering unrivalled depth and breadth of experience as a team.")
st.write("Chat privately with our AI about your background and MBA goals, to work out who is best placed to help you.")
st.warning('This demo AI agent is trained on fictional movie character data, rather than proprietary MBA consultant data.', icon="⚠️")

if "answers" not in st.session_state: 
    st.session_state.answers = []

client = OpenAI(api_key=st.secrets["openai_key"])
def submit_enquiry():
    enquiry = f"I need help applying to MBA schools. My goals are: {goals}. My background: {background}."

    prompt = f"You are the receptionist at Fortuna Admissions, the dream team of fictional movie characters and former Admissions Directors from the world\'s top business schools, providing advisory services to help MBA applicants strengthen their profile, position their application and target the best schools. Respond to the following enquiry from an MBA applicant with 3 answers, each from a fictional movie character {version}, each giving an in-character response to the enquiry. For each response, introduce yourself, compliment the applicant on a particular aspect of their background or experience, and explain how your own experience is relevant to helping the applicant, then explain the help available, including essay editing and mock interviews, asking an insightful and deeply probing hypothetical question about the background of the applicant as an example of what might be asked for an essay or mock interview. Finally mention a precise upcoming time in {country} when you are available for a consultation, and ask for the applicant to provide contact details as a next step. Separate each response with the string <hr>. Here's the enquiry: {enquiry}."

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    response_dict = ai_response.model_dump()
    message_content = response_dict["choices"][0]["message"]["content"]

    st.session_state.answers = message_content.split('<hr>')


background = st.text_area('Tell us about yourself. Copy & paste some excerpts from your resume or LinkedIn profile, or write a brief summary of your interests and achievements. Your name and contact details are not required.')

if background:
    goals = st.text_area('Great! What are your MBA goals? Are there specific schools and programs that have captured your attention?')

    if goals:
        country = st.selectbox(
            'Fantastic! Final question: what\'s your country of residence?',
            ['Australia', 'United States']
        )

        submit_button = st.button('Submit', type="primary", on_click=submit_enquiry, disabled=not country)

    else:
        goals_next = st.button('Next', type="primary")

else:
    background_next = st.button('Next', type="primary")

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
                st.html('<a href="https://fortunaadmissions.com/team-member/heidi-hillis/" target="_blank"><img src="https://poetsandquants.com/wp-content/uploads/sites/5/2015/11/Headshots-420x420.jpg" width="100%" /></a>')

            st.markdown(answer, unsafe_allow_html=True)

            name = st.text_input('Name', key=f'name-{idx}')
            email = st.text_input('Email', key=f'email-{idx}')
            enquiry_button = st.button('Submit', key=f'submit-{idx}', type="primary")

            if 'Heidi Hillis' in answer:
                st.html('<hr>')
                st.html('<b>Recent reviews</b>')
                st.html('<em>"Excellent Advisor - Stanford GSB Admit (Class Of 2027)"</em>')
                st.html('⭐⭐⭐⭐⭐ <small><a href="https://poetsandquants.com/consultant/heidi-hillis/" target="_blank">3 weeks ago</a></small>')
                st.html('<em>"Best Coach I Could Have Asked For! Best Coach! (Stanford / Columbia)"</em>')
                st.html('⭐⭐⭐⭐⭐ <small><a href="https://poetsandquants.com/consultant/heidi-hillis/" target="_blank">1 month ago</a></small>')
                st.html('<a href="https://poetsandquants.com/consultant/heidi-hillis/" target="_blank">More...</a>')

                st.html('<hr>')
                st.html('<b>Recent articles by Heidi</b>')
                st.html('<a href="https://fortunaadmissions.com/how-to-create-a-career-vision-for-your-mba-application/" target="_blank">How to Create a Career Vision For Your MBA Application</a>')
                st.html('<a href="https://fortunaadmissions.com/how-to-create-an-mba-career-vision-long-term-vs-short-term-goals/" target="_blank">MBA Goals: Long Term Vs. Short Term Career Vision</a>')
                st.html('<a href="https://fortunaadmissions.com/author/heidi/" target="_blank">More...</a>')
