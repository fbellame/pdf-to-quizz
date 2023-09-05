from qcm_chain import QCMGenerateChainTGI, QCMGenerateChainOpenAI
from qa_llm import QaLlmOpenAI, QaLlmTGI
from langchain.output_parsers.regex import RegexParser
from typing import List
from openllm_chain import OpenLlamaChain
import json
from quizz_utils import answer_check, filter_str

parsers = {
    "question": RegexParser(
        regex=r"question:(.*?)\?",
        output_keys=["question"]
    ),
    "choice_a": RegexParser(
        regex=r"CHOICE_A:(.*?)\\n",
        output_keys=["choice_a"]
    ),
    "choice_b": RegexParser(
        regex=r"CHOICE_B:(.*?)\\n",
        output_keys=["choice_b"]
    ),
    "choice_c": RegexParser(
        regex=r"CHOICE_C:(.*?)\\n",
        output_keys=["choice_c"]
    ),
    "choice_d": RegexParser(
        regex=r"CHOICE_D:(.*?)\\n",
        output_keys=["choice_d"]
    ),
    "answer": RegexParser(
        regex=r"reponse:(.*?)\\n",
        output_keys=["answer"]
    )
}

qa_llm_tgi = QaLlmTGI()
qa_chain_tgi = QCMGenerateChainTGI.from_llm(qa_llm_tgi.get_llm())

qa_llm_openai = QaLlmOpenAI()
qa_chain_openai = QCMGenerateChainOpenAI.from_llm(qa_llm_openai.get_llm())

def llm_call_tgi(qa_chain: OpenLlamaChain, texts: List[str]):
    
    print(f"llm call running...")
    batch_examples = qa_chain.predict_batch(texts, parsers)
    print(f"llm call done.")

    return batch_examples

def llm_call_openai(qa_chain: QCMGenerateChainOpenAI, text: str):
    
    print(f"llm call running...")
    batch_examples = qa_chain.apply_and_parse(text)
    print(f"llm call done.")

    print("check if answer if one of the choices a, b, c or d, if not try to find out the right choice from answer...")    
    resp = batch_examples[0].get("text")
    resp = filter_str(resp)
    try:
        js = json.loads(resp)
    except:
        js = {"question" : resp, "choice_a": "", "choice_b": "", "choice_c": "", "choice_d": "", "answer": ""}
    return answer_check(js)

def generate_quizz(contents:List[str]):
    """
    Generates a quizz from the given content.
    """
    docs = []
    openai_result = []
    docs = [{"doc": contents[0]}]
    openai_result.append(llm_call_openai(qa_chain_openai, docs))

    tgi_results = llm_call_tgi(qa_chain_tgi, docs)

    return {"context": docs[0]["doc"],"tgi": tgi_results[0], "openai": openai_result[0]}

    

    
