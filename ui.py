import streamlit as st
from ui_utils import check_password
from pdf_to_quizz import pdf_to_quizz
import asyncio

st.title("PDF to Quiz (:-)(-: )")

def build_question(count, json_question):

    if json_question.get(f"question") is not None:
        st.write("Question: ", json_question.get(f"question", ""))
        choices = ['A', 'B', 'C', 'D']
        selected_answer = st.selectbox(f"Selectionnez votre réponse:", choices, key=f"select_{count}")
        for choice in choices:
            choice_str = json_question.get(f"{choice}", "None")
            st.write(f"{choice} {choice_str}")
                    
        color = ""
        if st.button("Soumettre", key=f"button_{count}"):
            rep = json_question.get(f"reponse")
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

if uploaded_file is not None:    
    old_file_name = st.session_state.get('uploaded_file_name', None)
    if (old_file_name != uploaded_file.name):
        # Convert PDF to text
        with st.spinner("Génération du quizz..."):


            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            st.write("Quizz généré avec succès!")

            # Initialize session state
            st.session_state['uploaded_file_name'] = uploaded_file.name
            st.session_state['questions'] = asyncio.run(pdf_to_quizz(uploaded_file.name))

if ('questions' in st.session_state):
    # Display question
    count = 0
    for json_question in st.session_state['questions']:

        count = build_question(count, json_question)
