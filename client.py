import requests
import json

template = """<|prompt|>You are a teacher preparing questions for a quiz. Given the following document, please generate 1 multiple-choice questions (MCQs) with 4 options and a corresponding answer letter based on the document.
    Example question:
    Question: question here
    CHOICE_A: choice here
    CHOICE_B: choice here
    CHOICE_C: choice here
    CHOICE_D: choice here
    Answer: A or B or C or D
    <Begin Document>
    {doc}
    <End Document></s><|answer|>"""

url = 'http://192.168.1.138:8000/predict'
headers = {'Content-Type': 'application/json'}

def predict(prompt: str) -> str:
    try:
        cleaned_prompt = " ".join(template.format(doc=prompt).split())
        data = {'prompt': cleaned_prompt}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_data = response.json()

        if response.status_code == 200:
            return response_data["prediction"]
        else:
            print("Error: Status Code", response.status_code)
            print("Response:")
            print(json.dumps(response_data, indent=2))
    except requests.exceptions.RequestException as e:
        print("Error:", e)

    return "" 

print(predict("Audi finance must send me the quittance by next week with a check of 100$"))


