import streamlit as st
from ui_utils import check_password
from pdf_to_quizz import pdf_to_quizz
from text_to_quizz import txt_to_quizz
from generate_pdf import generate_pdf_quiz
import qcm_chain

st.title("PDF to Quiz RLHF: choose better quizz, local model or OpenAI GPT 3.5?")

# Upload PDF file
uploaded_file = st.file_uploader(":female-student:", type=["pdf"])

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

            st.session_state['questions'] = pdf_to_quizz(f"data/{uploaded_file.name}", quizz_progress_bar, 0, 3)

            st.write("Quizz généré avec succès!")

def build_question(count, json_question):

    decoder = {'choice_a': 'A', 'choice_b': 'B', 'choice_c': 'C', 'choice_d': 'D', 'A': 'A', 'B' : 'B', 'C': 'C', 'D': 'D', 'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}

    if json_question.get(f"question") is not None:
        st.write(":blue[Question:] ", json_question.get(f"question", "") + "?")
        choices = ['A', 'B', 'C', 'D']
        for choice in choices:
            decoded_choice = "choice_" + choice.lower()
            choice_str = json_question.get(f"{decoded_choice}", "None")
            st.write(f":blue[{choice}:] {choice_str}")

        st.write(":blue[Answer:] ", decoder[json_question.get(f"answer", "")])
        count += 1

    return count

def build_quizz(placeholder, count, quizz):


    with placeholder.container():

        st.header(':red[----------------------------------------------------]')

        st.write(":blue[**Context:**] " + quizz["context"])

        st.write(":green[**Local:**] ")
        count = build_question(count, quizz["tgi"])

        st.write(":red[**OPEN AI:**] ")
        count = build_question(count, quizz["openai"])

        selected_answer = st.selectbox(f"Selectionnez votre réponse:", ["local", "openai"], key=f"select_{count}")

        if st.button("Soumettre", key=f"button_{count}"):
            st.write(f":red[Vous avez choisi {selected_answer}].")    
            with open(f"data/dpo_dataset.csv", "a", encoding="latin-1", errors="ignore") as f:
                question = qcm_chain.template.format(doc=quizz["context"])
                good = "openai"
                bad = "tgi"
                if selected_answer == "local":
                    good = "tgi"
                    bad = "openai"
                    
                f.write(f"\"{question}\",{quizz[good]},{quizz[bad]}\n")

                del st.session_state[f"button_{count}"]

    return count

def generate_next_quizz(quizzs, count):
    # Display question
    for quizz in quizzs:
        placeholder = st.empty()
        count = build_quizz(placeholder, count, quizz)

    return count

count = 0
if ('questions' in st.session_state):

    count = generate_next_quizz(st.session_state['questions'], count)
        
    # generate pdf quiz
    if st.button("Get next Quizz questions...", key=f"button_next_quiz"):
        with st.spinner("Générer d'autres quizz..."):
            progress_text = "Operation en cours..."
            quizz_progress_bar = st.progress(0, text=progress_text)
            st.session_state['questions'] = pdf_to_quizz(f"data/{uploaded_file.name}", quizz_progress_bar, 3, 6)
            
            count = generate_next_quizz(st.session_state['questions'], count)