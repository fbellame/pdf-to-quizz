from mistral_inference import MistralTextGenInference

url = "https://75syq57x8ohyw7-8000.proxy.runpod.net/"
mistral = MistralTextGenInference(inference_server_url=url, max_new_tokens=500, temperature=0.1)

def llm_call(text: str):
    
    print("llm call running...")
    result = mistral(text)
    print("llm call done.")

    return result

def generate_quizz(content:str):
    """
    Generates a quizz from the given content.
    """
    return llm_call(content)

    
