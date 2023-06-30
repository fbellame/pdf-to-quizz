from langchain.document_loaders import PyPDFLoader
from quizz_generator import generate_quizz
from langchain.text_splitter import NLTKTextSplitter

def pdf_to_quizz(pdf_file_name):

    loader = PyPDFLoader(pdf_file_name)

    docs = loader.load_and_split(NLTKTextSplitter(chunk_size=700, chunk_overlap=0))
    paragraphs =list(map(lambda doc: doc.page_content.replace("\n", " ").strip(), docs))

    tasks = []
    i = 0
    for paragraph in paragraphs:
        i+=1
        try:
            if i<=10:
                task = process_paragraph(paragraph)
                tasks.append(task)
            else:
                break
        except Exception as e:
            # Handle the exception
            print(f"Error processing page: {str(e)}")
            # Optionally, you can choose to skip the page and continue with the next one
            continue        

    return tasks
  
def process_paragraph(paragraph):
    return  generate_quizz(paragraph)
