import streamlit as st
from ui_utils import check_password
from pdf_to_quizz import pdf_to_quizz
from text_to_quizz import txt_to_quizz
from generate_pdf import generate_pdf_quiz
import qcm_chain
import dummy
import base64

QUIZZ_SIZE = 2
QUIZZ_LAST = 2

class QuizzItem():

    def __init__(self, question, visible):
        self.question = question
        self.visible = visible

class Quizz():

    def __init__(self, quizz_list) -> None:
        self.quizz_list = quizz_list

def decode(answer):
    decoder = {'choice_a': 'A', 'choice_b': 'B', 'choice_c': 'C', 'choice_d': 'D', 'A': 'A', 'B' : 'B', 'C': 'C', 'D': 'D', 'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}

    try:
        return decoder[answer]
    except:
        return answer
    
def build_question(count, json_question):

    if json_question.get("question") is not None:
        st.write(":blue[Question:] ", json_question.get("question", "") + "?")
        choices = ['A', 'B', 'C', 'D']
        for choice in choices:
            decoded_choice = "choice_" + choice.lower()
            choice_str = json_question.get(f"{decoded_choice}", "None")
            st.write(f":blue[{choice}:] {choice_str}")

        st.write(":blue[Answer:] ", decode(json_question.get("answer", "")))
        count += 1

    return count

def build_quizz(count: int, quizz_item: QuizzItem) -> int:

    if quizz_item.visible:
        st.header(':red[----------------------------------------------------]')

        st.write(":blue[**Context:**] " + quizz_item.question["context"])

        st.write(":green[**Local:**] ")
        count = build_question(count, quizz_item.question["tgi"])

        st.write(":red[**OPEN AI:**] ")
        count = build_question(count, quizz_item.question["openai"])

        selected_answer = st.selectbox("Do you prefer :green[**Local:**] or :red[**OPEN AI:**] quiz?", ["local", "openai"], key=f"select_{count}")

        if st.button("Submit", key=f"button_{count}"):
            st.write(f":red[You prefer {selected_answer}].")    
            with open("data/dpo_dataset.csv", "a", encoding="latin-1", errors="ignore") as f:
                question = qcm_chain.template.format(doc=quizz_item.question["context"])
                good = "openai"
                bad = "tgi"
                if selected_answer == "local":
                    good = "tgi"
                    bad = "openai"
                    
                f.write(f"\"{question}\",{quizz_item.question[good]},{quizz_item.question[bad]}\n")

                quizz_item.visible = False
                with open("dummy.py", "w") as f:
                    f.write("# refresh please")

    return count

def display_pdf(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

def generate_next_quizz(count: int, quizz: Quizz) -> int:

    quizz_list = quizz.quizz_list
    # Display question
    for quizz_item in quizz_list:
        count = build_quizz(count, quizz_item)

    return count

def quizz_list(questions):
    quizzList = []
    for question in questions:
        quizzList.append(QuizzItem(question, True))
    return Quizz(quizzList)

st.title("PDF to Quiz: choose better quizz, local model or OpenAI GPT 3.5?")

# Upload PDF file
uploaded_file = st.file_uploader(":female-student:", type=["pdf"])

if uploaded_file is not None:    
    old_file_name = st.session_state.get('uploaded_file_name', None)
    if (old_file_name != uploaded_file.name):
        # Convert PDF to text
        with st.spinner("Generation of 3 quizz..."):

            progress_text = "Operation en cours..."
            quizz_progress_bar = st.progress(0, text=progress_text)

            with open(f"data/{uploaded_file.name}", "wb") as f:
                f.write(uploaded_file.getvalue())        

            # Initialize session state
            st.session_state['uploaded_file_name'] = uploaded_file.name

            try:
                quizz = quizz_list(pdf_to_quizz(f"data/{uploaded_file.name}", quizz_progress_bar, 0, QUIZZ_LAST))
                st.session_state['quizz'] = quizz
                st.write("Quizz generated with succes!")
            except:
                st.write("Impossible to read the PDF")
                uploaded_file = "error"

count = 0
if ('quizz' in st.session_state):

    quizz = st.session_state['quizz']

    display_pdf(f"data/{uploaded_file.name}")

    count = generate_next_quizz(count, quizz)
        
    # generate pdf quiz
    if st.button("Get next Quizz questions...", key="button_next_quiz"):
        with st.spinner("Generate 3 other quizz..."):
            progress_text = "Progess..."
            quizz_progress_bar = st.progress(0, text=progress_text)
            st.session_state['quizz'] = quizz_list(pdf_to_quizz(f"data/{uploaded_file.name}", quizz_progress_bar, QUIZZ_LAST, (QUIZZ_LAST + QUIZZ_SIZE)))
            QUIZZ_LAST += QUIZZ_SIZE
            
            count = generate_next_quizz(count, st.session_state['quizz'])