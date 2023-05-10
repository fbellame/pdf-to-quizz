import asyncio
from quizz_generator import generate_quizz
from ui_utils import transform

async def txt_to_quizz(content):

    quizz = await generate_quizz(content)
    if quizz is not None:
        trasnformed_quizz = transform(quizz[0])
        return trasnformed_quizz

    return ''

