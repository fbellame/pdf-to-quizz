import re
import json

def filter_str(input):

    # Replace special characters with a space, except for line breaks
    s1=re.sub("[^A-Za-z?@.!$%*-+,]"," ",input)

    # Collapse multiple spaces into one
    return re.sub(r'\s+', ' ', s1)



def filter_str(input):

    # Replace special characters with a space, except for line breaks
    s1=re.sub("[^A-Za-z?@.!$%*-+_\",()\]\[:{}]"," ",input)

    # Collapse multiple spaces into one
    return re.sub(r'\s+', ' ', s1)


print(filter_str('\n\n{\n  "question": "According to the document, what is the purpose of the teacher?",\n  "choice_a": "Preparing questions for a quiz",\n  "choice_b": "Grading student assignments",\n  "choice_c": "Organizing extracurricular activities",\n  "choice_d": "Attending a conference",\n  "answer": "choice_a"\n}'))
#data = '\n\n{\n  "question": "According to the document, what is the purpose of the teacher?",\n  "choice_a": "Preparing questions for a quiz",\n  "choice_b": "Grading student assignments",\n  "choice_c": "Organizing extracurricular activities",\n  "choice_d": "Attending a conference",\n  "answer": "choice_a"\n}'

#js = json.loads(data)

#print(js)

