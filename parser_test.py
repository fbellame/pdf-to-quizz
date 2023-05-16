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
input_string = '''Question: What is the main contribution of the paper?
CHOICE_A: Introducing a hybrid architecture combining deep learning layers with a final discrete NP-hard Graphical Model reasoning layer
CHOICE_B: Proposing a new loss function that efficiently deals with logical information
CHOICE_C: Using discrete GMs as the reasoning language
CHOICE_D: All of the above
Answer: D

Question: What type of problems can the proposed neural architecture and loss function efficiently learn to solve?
CHOICE_A: Only visual problems
CHOICE_B: Only symbolic problems
CHOICE_C: Only energy optimization problems
CHOICE_D: NP-hard reasoning problems expressed as discrete Graphical Models, including symbolic, visual, and energy optimization problems
Answer:D
'''

output_parser = RegexParser(
    regex=r"Question\s?\d?:\s+\n?(.*?)\nCHOICE_A(.*?)\nCHOICE_B(.*?)\nCHOICE_C(.*?)\nCHOICE_D(.*?)(?:\n)+Answer:\s?(.*)\n?\n?Question\s?\d?:\s+\n?(.*?)\nCHOICE_A(.*?)\nCHOICE_B(.*?)\nCHOICE_C(.*?)\nCHOICE_D(.*?)(?:\n)+Answer:\s?(.*)", 
    output_keys=["question1", "A_1", "B_1", "C_1", "D_1", "reponse1","question2", "A_2", "B_2", "C_2", "D_2", "reponse2"]
)

# Use the RegexParser to parse the input string
output_dict = transform(output_parser.parse(input_string))



# Print the parsed output
print(output_dict)

