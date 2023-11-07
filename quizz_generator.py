import os
from runpod_proxy import RunProxyClass

inference_params = {
    'max_new_tokens': 500,
    'temperature': 0.1
}

run_proxy = RunProxyClass(inference_params)

def llm_call(text: str):
    print("llm call running...")
    result = run_proxy.generate_text(text)
    print("llm call done.")
    return result

def generate_quizz(content: str):
    """
    Generates a quizz from the given content.
    """
    return llm_call(content)


    
