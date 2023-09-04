import streamlit as st
from ui_utils import check_password
from pdf_to_quizz import pdf_to_quizz
from text_to_quizz import txt_to_quizz
from generate_pdf import generate_pdf_quiz
import json

st.title("PDF to Quiz (:-)(-: )")


def build_question(count, json_question):

    if json_question.get(f"question") is not None:
        st.write("Question: ", json_question.get(f"question", "") + "?")
        choices = ['choice_a', 'choice_b', 'choice_c', 'choice_d']
        selected_answer = st.selectbox(f"Selectionnez votre réponse:", choices, key=f"select_{count}")
        for choice in choices:
            choice_str = json_question.get(f"{choice}", "None")
            st.write(f"{choice}: {choice_str}")
                    
        color = ""
        if st.button("Soumettre", key=f"button_{count}"):
            rep = json_question.get(f"answer")
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

if st.button("Générer Quiz", key=f"button_generer"):
    if txt is not None:
        with st.spinner("Génération du quizz..."):

            st.session_state['questions'] = txt_to_quizz(txt)
            st.write("Quizz généré avec succès!")

if uploaded_file is not None:    
    old_file_name = st.session_state.get('uploaded_file_name', None)
    if (old_file_name != uploaded_file.name):
        # Convert PDF to text
        with st.spinner("Génération du quizz..."):

            progress_text = "Operation en cours..."
            quizz_progress_bar = st.progress(0, text=progress_text)

            with open(f"data/{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getvalue())        

            # Initialize session state
            st.session_state['uploaded_file_name'] = uploaded_file.name
            st.session_state['questions'] = pdf_to_quizz(f"data/{uploaded_file.name}", quizz_progress_bar)

            st.write("Quizz généré avec succès!")

def build_quizz(count, quizz):
    st.write("**Context:** " + quizz["context"])

    st.write("**TGI:** ")
    count = build_question(count, quizz["tgi"])

    st.write("**OPEN AI:** ")
    count = build_question(count, quizz["openai"])

    return count


if ('questions' in st.session_state):
    # Display question
    count = 0
    for quizz in st.session_state['questions']:
        count = build_quizz(count, quizz)
        
    # generate pdf quiz
    if st.button("Générer PDF Quiz", key=f"button_generer_quiz"):
        with st.spinner("Génération du quizz en PDF..."):
            json_questions = st.session_state['questions']
            # save into a file
            file_name = uploaded_file.name

            # remove extension .pdf from file name
            if file_name.endswith(".pdf"):
                file_name = file_name[:-4]

            with open(f"data/quiz-{file_name}.json", "w", encoding='latin-1', errors='ignore') as f:
                str = json.dumps(json_questions)
                f.write(str)

            generate_pdf_quiz(f"data/quiz-{file_name}.json", json_questions)
            
            st.write("PDF Quiz généré avec succés!")        