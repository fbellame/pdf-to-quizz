from langchain.output_parsers.regex import RegexParser

def transform(input_list):
    new_list = []
    for key in input_list:
        if 'question1' in key or 'question2' in key:
            question_dict = {}
            question_num = key[-1]
            question_dict[f'question'] = input_list[key]
            question_dict[f'A'] = input_list[f'A_{question_num}']
            question_dict[f'B'] = input_list[f'B_{question_num}']
            question_dict[f'C'] = input_list[f'C_{question_num}']
            question_dict[f'D'] = input_list[f'D_{question_num}']
            question_dict[f'reponse'] = input_list[f'reponse{question_num}']
            new_list.append(question_dict)
    return new_list

# Define input string to parse
#input_string = "Question 1: What is the conclusion of the study regarding the use of pretrained weights on 2D-Slice models with ResNet encoders initialized with ImageNet-1K pretrained weights for 3D Deep Neuroimaging?\nCHOIX_A: Pretrained weights consistently underperforms random initialization\nCHOIX_B: Pretrained weights consistently outperforms random initialization\nCHOIX_C: Pretrained weights have no effect on the performance of the models\nCHOIX_D: The study did not test the use of pretrained weights on 2D-Slice models\n\nRéponse: B\n\nQuestion 2: What is the main hypothesis that the study validates?\nCHOIX_A: Models trained on natural images (2D) cannot be helpful for neuroimaging tasks\nCHOIX_B: Models trained on natural images (2D) can be helpful for neuroimaging tasks\nCHOIX_C: 2D-Slice-CNNs cannot be used for neuroimaging tasks\nCHOIX_D: 2D-Slice-CNNs are the only models that can be used for neuroimaging tasks\n\nRéponse: B"
# doc = '''question :      What was the reason for not asking for the LLM-based condition to show its work in the preliminary work on the paper?


#  CHOICE_A:     The author thought it would increase the likelihood of transcribing the wrong answer.
#  CHOICE_B:    The author wanted to avoid confusing the participant with a lot of numbers.
#  CHOICE_C:    The author believed that precise probabilities had nothing to do with the problem.
#  CHOICE_D:The author wanted to use a meta-prompt that didn't require determining precise probabilities.


# reponse: B


# '''

doc = 'question: What is the purpose of the get_parsed_value function in the given document?\r\n CHOICE_A: To parse the value based on the given parser and document.\r\n CHOICE_B: To merge the parsed values into the quizz dictionary.\r\n CHOICE_C: To create a new dictionary called parsers.\r\n CHOICE_D: To define a new function called update method.\r\nreponse: A\r\n\r\r'

parsers = {
    "question": RegexParser(
        #regex=r"question\s+:\s+\n?(.*?)(?:\n)+",
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

def get_parsed_value(parser, key, doc):
    result = parser.parse(doc)
    value = result.get(key).strip()
    return {key: value}

quizz = {}
for key, parser in parsers.items():
    quizz.update(get_parsed_value(parser, key, doc))

quizz_list = [quizz]

output_parser = RegexParser(
    regex=r"question\s?\d?:\s+\n?(.*?)\n\s*CHOICE_A(.*?)\n\s*CHOICE_B(.*?)\n\s*CHOICE_C(.*?)\n\s*CHOICE_D(.*?)(?:\n)+reponse:\s?(.*)", 
    output_keys=["question1", "A_1", "B_1", "C_1", "D_1", "reponse1"]
)

# Use the RegexParser to parse the input string
output_dict = transform(output_parser.parse(doc))

# Print the parsed output
print(output_dict)

