from qcm_chain import QCMGenerateChain
from qa_llm import QaLlm
from langchain.output_parsers.regex import RegexParser

output_parser = RegexParser(
    regex=r"question:\s+\n?(.*?)(?:\n)+\s*CHOICE_A:(.*?)\n+\s*CHOICE_B:(.*?)\n+\s*CHOICE_C:(.*?)\n+\s*CHOICE_D:(.*?)(?:\n)+reponse:\s?(.*)", 
    output_keys=["question", "A", "B", "C", "D", "reponse"])

qa_llm = QaLlm()
qa_chain = QCMGenerateChain.from_llm(qa_llm.get_llm())

def llm_call(qa_chain: QCMGenerateChain, text: str):
    
    print(f"llm call running...")
    batch_examples = qa_chain.predict_and_parse(text, output_parser)
    print(f"llm call done.")

    return batch_examples

def generate_quizz(content:str):
    """
    Generates a quizz from the given content.
    """

    return llm_call(qa_chain, [{"doc": content}])

    
