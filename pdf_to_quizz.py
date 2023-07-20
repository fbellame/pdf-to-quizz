from langchain.document_loaders import PyPDFLoader
from quizz_generator import generate_quizz
from langchain.text_splitter import NLTKTextSplitter
import nltk
from typing import List

nltk.download('punkt')

def pdf_to_quizz(pdf_file_name):

    loader = PyPDFLoader(pdf_file_name)

    docs = loader.load_and_split(NLTKTextSplitter(chunk_size=700, chunk_overlap=0))
    paragraphs =list(map(lambda doc: doc.page_content.replace("\n", " ").strip(), docs))

    i = 0
    batch_paragraph : List[str] = []
    for paragraph in paragraphs:
        i+=1
        if i<=10:
            batch_paragraph.append(paragraph)
        else:
            break

    return generate_quizz(batch_paragraph)
  
# def process_paragraph(paragraph):
#     return  generate_quizz(paragraph)
