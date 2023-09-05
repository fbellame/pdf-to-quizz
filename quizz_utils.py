import re
#
# Check of answer if one of the choices a, b, c or d, if not try to find out the right choice from answer...
# quizz exemple:
#    {'question': 'Who are the instructors for MIT 6S191 introduction to deep learning?', 
#     'choice_a': 'Alexander Amini', 
#     'choice_b': 'Alva Solimani', 
#     'choice_c': 'Both Alexander Amini and Alva Solimani', 
#     'choice_d': 'None of the above', 
#     'answer': 'Both Alexander Amini and Alva Solimani'}
#
def answer_check(quizz):
    answer = quizz["answer"]
    choices = ['choice_a', 'choice_b', 'choice_c', 'choice_d']

    # check if answer is one of the 4 choices, choice_a, ...
    if not answer in choices:

        # no, OpenAI get it wrong, try to match answer to one of the 4 choices
        for choice in choices:
            if answer == quizz[choice]:
                quizz["answer"] = choice
                print(f"fixed quizz answer: {answer} by {choice}")
                break

    return quizz

def filter_str(input):

    # Replace special characters with a space, except for line breaks
    s1=re.sub("[^A-Za-z?@.!$%*-+_\",()\]\[:{}]"," ",input)

    # Collapse multiple spaces into one
    return re.sub(r'\s+', ' ', s1)