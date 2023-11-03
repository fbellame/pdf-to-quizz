"""Wrapper around Mistral Runpod text generation inference API."""
import requests
import json
from langchain.output_parsers.regex import RegexParser

template = """<s>[INST] You are a teacher preparing questions for a quiz. Given the following document, please generate 1 multiple-choice questions (MCQs) with 4 options and a corresponding answer letter based on the document.\\n\\nExample question:\\n\\nQuestion: question here\\nCHOICE_A: choice here\\nCHOICE_B: choice here\\nCHOICE_C: choice here\\nCHOICE_D: choice here\\nAnswer: A or B or C or D\\n\\nThese questions should be detailed and solely based on the information provided in the document.\\n here are the inputs \\n{doc}\\n[/INST]"""

url = 'https://75syq57x8ohyw7-8000.proxy.runpod.net/'
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

parsers = {
    "question": RegexParser(
        regex=r"question:(.*?)\?",
        output_keys=["question"]
    ),
    "A": RegexParser(
        regex=r"CHOICE_A:(.*?)\\n",
        output_keys=["A"]
    ),
    "B": RegexParser(
        regex=r"CHOICE_B:(.*?)\\n",
        output_keys=["B"]
    ),
    "C": RegexParser(
        regex=r"CHOICE_C:(.*?)\\n",
        output_keys=["C"]
    ),
    "D": RegexParser(
        regex=r"CHOICE_D:(.*?)\\n",
        output_keys=["D"]
    ),
    "reponse": RegexParser(
        regex=r"reponse:(.*?)\\n",
        output_keys=["reponse"]
    )
}

class MistralTextGenInference():
    """
    Mistral text generation inference API.

    This class is a wrapper around my Mistral RunPod text generation inference API.
    It is used to generate text from a given prompt.
                        
    """

    def __init__(self, inference_server_url, max_new_tokens, temperature):
        self.inference_server_url = inference_server_url    
        self.max_new_tokens: int = max_new_tokens
        self.temperature: float = temperature
        self.repetition_penalty: float = 1.2
        self.num_beams: int = 1

    def __call__(
        self,
        prompt: str,
    ):

        cleaned_prompt = " ".join(template.format(doc=prompt).split())
        data = {'prompt': cleaned_prompt, 'max_new_tokens': self.max_new_tokens, "temperature": self.temperature}

        try:
            endpoint = f"{self.inference_server_url}predict"
            payload = json.dumps(data)
           
            response = requests.post(endpoint, data=payload, headers=headers)
            response_data = response.json()

            if response.status_code == 200:
                return self.parse(response_data["prediction"])
            else:
                print("Error: Status Code", response.status_code)
                print("Response:")
                print(json.dumps(response_data, indent=2))
        except requests.exceptions.RequestException as e:
            print("Error:", e)

        return "" 
    
    def get_parsed_value(self, parser, key, doc):
        try:
            result = parser.parse(doc)
            value = result.get(key).strip()
            return {key: value}
        except Exception as e:
            print(f"Error processing doc: {str(e)}")
            print(f"Key {key}")
            return {key: "error"}    
        
    def parse(self, text: str):

        quizz = {}
        for key, parser in parsers.items():
            quizz.update(self.get_parsed_value(parser, key, text))
        quizz_list = [quizz]

        return quizz_list
    
if __name__ == "__main__":
    mistral = MistralTextGenInference(inference_server_url=url, max_new_tokens=500, temperature=0.1)

    print(mistral("Farid is a software developper passionate about generative AI. He was born in France in 1972"))


