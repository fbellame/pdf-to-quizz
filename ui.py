import streamlit as st
from ui_utils import check_password
from pdf_to_quizz import pdf_to_quizz
from text_to_quizz import txt_to_quizz
from quizz_to_form import GoogleForm

st.title("Welcome to PDF to Quiz (:-)(-: )")

if 'google_form' not in st.session_state:
    st.session_state['google_form'] = None  # Or the appropriate initial value

def build_question(count, json_question):

    if json_question.get("question") is not None:
        st.write("Question: ", json_question.get("question", ""))
        choices = ['A', 'B', 'C', 'D']
        selected_answer = st.selectbox("Please select a response:", choices, key=f"select_{count}")
        for choice in choices:
            choice_str = json_question.get(f"{choice}", "None")
            st.write(f"{choice} {choice_str}")
                    
        color = ""
        if st.button("Submit", key=f"button_{count}"):
            rep = json_question.get("reponse")
            if selected_answer == rep:
                color = ":green"
                st.write(f":green[Good answer: {rep}]")
                
            else:
                color = ":red"
                st.write(f":red[Bad answer. The good answer is {rep}].")                

        st.write(f"{color}[Your response: {selected_answer}]")

        count += 1

    return count

# Upload PDF file
uploaded_file = st.file_uploader(":female-student:", type=["pdf"])
txt = st.text_area('Type some text you want to generate a quizz with...')

if st.button("Generate Quiz", key="button_generer") and txt is not None:
    with st.spinner("Please wait a little bit while the quizz is generating, you you uploader a multi pages pdf it can be quite long, so grab a coffee..."):
        st.session_state['questions'] = txt_to_quizz(txt)
        st.write("Quizz generated with success!")

if uploaded_file is not None:    
    old_file_name = st.session_state.get('uploaded_file_name', None)
    if (old_file_name != uploaded_file.name):
        # Convert PDF to text
        with st.spinner("Please wait a little bit while the quizz is generating, you you uploader a multi pages pdf it can be quite long, so grab a coffee..."):

            with open(f"data/{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getvalue())        

            # Initialize session state
            st.session_state['uploaded_file_name'] = uploaded_file.name
            st.session_state['questions'] = pdf_to_quizz(f"data/{uploaded_file.name}")

            st.write("Quizz generated with success!")

if ('questions' in st.session_state):
    # Display question
    count = 0
    for json_question in st.session_state['questions']:

        count = build_question(count, json_question)
            
    # generate google form quiz :-)
    if st.button("Generate google form Quiz", key="button_google-form_quiz"):
        with st.spinner("Generation of the quizz Google Form..."):
            json_questions = st.session_state['questions']

            google_form = st.session_state['google_form']
            if google_form is None:
                google_form = GoogleForm()
                st.session_state['google_form'] = google_form

            result = google_form.quiz_to_form(json_questions)
            
            st.write("Google Form Quiz generated with success, click the link to access it!") 
            st.write(f'[PQF-to_quizz-form]({result["responderUri"]})')

