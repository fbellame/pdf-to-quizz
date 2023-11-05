from langchain.document_loaders import PyPDFLoader
from quizz_generator import generate_quizz
from ui_utils import transform

def pdf_to_quizz(pdf_file_name):

    loader = PyPDFLoader(pdf_file_name)
    pages = loader.load_and_split()

    def process_page(page):

            return generate_quizz(page.page_content)

    questions = []
    for page in pages:
        question = process_page(page)
        questions.append(question)

    all_questions = []
    
    for question in questions:
        all_questions.extend(transform(question))

    return all_questions
  
