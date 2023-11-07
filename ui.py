import streamlit as st
from ui_utils import check_password
from pdf_to_quizz import pdf_to_quizz
from text_to_quizz import txt_to_quizz
from quizz_to_form import GoogleForm

st.title("PDF to Quiz (:-)(-: )")

if 'google_form' not in st.session_state:
    st.session_state['google_form'] = None  # Or the appropriate initial value

def build_question(count, json_question):

    if json_question.get("question") is not None:
        st.write("Question: ", json_question.get("question", ""))
        choices = ['A', 'B', 'C', 'D']
        selected_answer = st.selectbox("Selectionnez votre réponse:", choices, key=f"select_{count}")
        for choice in choices:
            choice_str = json_question.get(f"{choice}", "None")
            st.write(f"{choice} {choice_str}")
                    
        color = ""
        if st.button("Soumettre", key=f"button_{count}"):
            rep = json_question.get("reponse")
            if selected_answer == rep:
                color = ":green"
                st.write(f":green[Bonne réponse: {rep}]")
                
            else:
                color = ":red"
                st.write(f":red[Mauvause réponse. La bonne réponse est {rep}].")                

        st.write(f"{color}[Votre réponse: {selected_answer}]")

        count += 1

    return count

# Upload PDF file
uploaded_file = st.file_uploader(":female-student:", type=["pdf"])
txt = st.text_area('Taper le texte à partir duquel vous voulez générer le quizz')

if st.button("Générer Quiz", key="button_generer") and txt is not None:
    with st.spinner("Génération du quizz..."):
        st.session_state['questions'] = txt_to_quizz(txt)
        st.write("Quizz généré avec succès!")

if uploaded_file is not None:    
    old_file_name = st.session_state.get('uploaded_file_name', None)
    if (old_file_name != uploaded_file.name):
        # Convert PDF to text
        with st.spinner("Génération du quizz..."):

            with open(f"data/{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getvalue())        

            # Initialize session state
            st.session_state['uploaded_file_name'] = uploaded_file.name
            st.session_state['questions'] = pdf_to_quizz(f"data/{uploaded_file.name}")

            st.write("Quizz généré avec succès!")

if ('questions' in st.session_state):
    # Display question
    count = 0
    for json_question in st.session_state['questions']:

        count = build_question(count, json_question)
            
    # generate google form quiz :-)
    if st.button("Générer google form Quiz", key="button_google-form_quiz"):
        with st.spinner("Génération du quizz Google Form..."):
            json_questions = st.session_state['questions']

            google_form = st.session_state['google_form']
            if google_form is None:
                google_form = GoogleForm()
                st.session_state['google_form'] = google_form

            result = google_form.quiz_to_form(json_questions)
            
            st.write("Google Form Quiz généré avec succés!") 
            st.write(f'[PQF-to_quizz-form]({result["responderUri"]})')

