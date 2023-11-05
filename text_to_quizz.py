from quizz_generator import generate_quizz
from ui_utils import transform

def txt_to_quizz(content):

    quizz = generate_quizz(content)
    if quizz is not None:
        trasnformed_quizz = transform(quizz)
        return trasnformed_quizz

    return ''

