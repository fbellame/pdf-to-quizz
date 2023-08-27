from langchain.llms import HuggingFaceTextGenInference
from langchain.output_parsers.regex import RegexParser

llm = HuggingFaceTextGenInference(
    inference_server_url="http://localhost:8080/",
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.03,
)

#doc = "Louis IX was only twelve years old when he became King of France. His mother — Blanche of Castile — was the effective power as regent (although she did not formally use the title). Blanche's authority was strongly opposed by the French barons yet she maintained her position until Louis was old enough to rule by himself."
doc = "Farid est un développeur logiciel né en 1972. Il a eu son premier ordinateur à l'age de 10 ans."

template = "|system|You are a teacher preparing questions for a quiz. Given the following document, please generate 1 multiple-choice questions (MCQs) with 4 options and a corresponding answer letter based on the document.\\nExample question:\\nQuestion: question here\\nCHOICE_A: choice here\\nCHOICE_B: choice here\\nCHOICE_C: choice here\\nCHOICE_D: choice here\\nAnswer: A or B or C or D\\nThese questions should be detailed and solely based on the information provided in the document:  |prompt|\\n{doc}\\n\\n |answer|"

formated_doc = template.format(doc=doc)

reponse = llm(formated_doc)
#reponse = "question: Quel âge avait Farid lorsqu'il a eu son premier ordinateur ?\nCHOICE_A: 15 ans\nCHOICE_B: 10 ans\nCHOICE_C: 20 ans\nCHOICE_D: 30 ans\nreponse: B\n"
#reponse = "question: Quel âge avait Farid lorsqu'il a eu son premier ordinateur ?\\nCHOICE_A: 15 ans\\nCHOICE_B: 10 ans\\nCHOICE_C: 20 ans\\nCHOICE_D: 30 ans\\nreponse: B\\n"

print(reponse)

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


def get_parsed_value(parser, key, doc):
    try:
        result = parser.parse(doc)
        value = result.get(key).strip()
        return {key: value}
    except Exception as e:
        print(f"Error processing doc: {str(e)}")
        print(f"Key {key}")
        return {key: "error"}
    

quizz = {}
for key, parser in parsers.items():
    quizz.update(get_parsed_value(parser, key, reponse))

quizz_list = [quizz]

# Print the parsed output
print(quizz_list)