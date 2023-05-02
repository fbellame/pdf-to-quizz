import asyncio
from qa_llm import QaLlm
from qcm_chain import QCMGenerateChain
from langchain.document_loaders import PyPDFLoader

async def llm_call(qa_chain: QCMGenerateChain, text: str):
    
    print(f"llm call running...")
    batch_examples = await asyncio.gather(qa_chain.aapply_and_parse(text))
    print(f"llm call done.")

    return batch_examples

async def pdf_to_quizz(pdf_file_name):

    qa_llm = QaLlm()
    qa_chain = QCMGenerateChain.from_llm(qa_llm.get_llm())

    loader = PyPDFLoader(pdf_file_name)
    pages = loader.load_and_split()

    sem = asyncio.Semaphore(10)  # Set the maximum number of parallel tasks

    async def process_page(page):
        async with sem:
            return await llm_call(qa_chain, [{"doc": page.page_content}])

    tasks = []
    for page in pages:
        task = process_page(page)
        tasks.append(task)

    all_questions = []

    questions = await asyncio.gather(*tasks)    
    
    for question in questions:
        all_questions.extend(transform(question[0]))

    return all_questions

def transform(input_list):
    new_list = []
    for item in input_list:
        for key in item:
            if 'question1' in key or 'question2' in key or 'question3' in key:
                question_dict = {}
                question_num = key[-1]                
                question_dict[f'question'] = item[key]
                question_dict[f'A'] = item[f'A_{question_num}']
                question_dict[f'B'] = item[f'B_{question_num}']
                question_dict[f'C'] = item[f'C_{question_num}']
                question_dict[f'D'] = item[f'D_{question_num}']
                question_dict[f'reponse'] = item[f'reponse{question_num}']
                new_list.append(question_dict)
    return new_list    
