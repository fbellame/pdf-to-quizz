from qcm_chain import QCMGenerateChain
from qa_llm import QaLlm
from langchain.output_parsers.regex import RegexParser
from typing import List

parsers = {
    "question": RegexParser(
        regex=r"question:\s*(.*?)\s+(?:\n)+",
        output_keys=["question"]
    ),
    "A": RegexParser(
        regex=r"(?:\n)+\s*CHOICE_A:(.*?)\n+",
        output_keys=["A"]
    ),
    "B": RegexParser(
        regex=r"(?:\n)+\s*CHOICE_B:(.*?)\n+",
        output_keys=["B"]
    ),
    "C": RegexParser(
        regex=r"(?:\n)+\s*CHOICE_C:(.*?)\n+",
        output_keys=["C"]
    ),
    "D": RegexParser(
        regex=r"(?:\n)+\s*CHOICE_D:(.*?)\n+",
        output_keys=["D"]
    ),
    "reponse": RegexParser(
        regex=r"(?:\n)+reponse:\s?(.*)",
        output_keys=["reponse"]
    )
}

qa_llm = QaLlm()
qa_chain = QCMGenerateChain.from_llm(qa_llm.get_llm())

def llm_call(qa_chain: QCMGenerateChain, texts: List[str]):
    
    print(f"llm call running...")
    batch_examples = qa_chain.predict_batch(texts, parsers)
    print(f"llm call done.")

    return batch_examples

def generate_quizz(contents:List[str]):
    """
    Generates a quizz from the given content.
    """
    docs = []
    for content in contents:
        docs.append({"doc": content})

    return llm_call(qa_chain, docs)

    
