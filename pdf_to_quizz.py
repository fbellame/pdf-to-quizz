from quizz_generator import generate_quizz
from ui_utils import transform
from PyPDF2 import PdfReader

def pdf_to_quizz(pdf_file_name):

    reader = PdfReader(pdf_file_name)
    pages = reader.pages

    def process_page(page):
        return generate_quizz(page.extract_text().replace("\n", " ").strip())

    questions = []
    for page in pages:
        question = process_page(page)
        questions.append(question)

    all_questions = []
    
    for question in questions:
        all_questions.extend(transform(question))

    return all_questions
  
