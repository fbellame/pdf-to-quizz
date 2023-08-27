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

    quizzs = []

    for i in range(0, len(paragraphs), 2):
        batch_paragraph : List[str] = []
        if i + 1 < len(paragraphs):
            batch_paragraph = paragraphs[i:i+2]
        else:
            batch_paragraph = [paragraphs[i]]
        quizzs.extend(generate_quizz(batch_paragraph))

        # max 10 quizzs
        if len(quizzs)> 10:
            break

    return quizzs
  
