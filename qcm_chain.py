"""LLM Chain specifically for generating examples for QCM (Question Choix Multiples) answering."""
from __future__ import annotations

from typing import Any

from langchain.chains.llm import LLMChain
from langchain.llms.base import BaseLLM
from langchain.output_parsers.regex import RegexParser

from langchain.prompts import PromptTemplate

template = """Vous êtes un enseignant qui prépare des questions pour un quiz.
Étant donné le document suivant, veuillez générer 2 questions de type QCM avec 4 options et une réponse qui correspond à la lettre du bon choix du QCM basées sur ce document.

Exemple question:

Question: question ici
CHOIX_A: choix ici
CHOIX_B: choix ici
CHOIX_C: choix ici
CHOIX_D: choix ici
Réponse: réponse A ou B ou C ou D

Ces questions devraient être détaillées et uniquement basées sur les information dans le document.

<Begin Document>
{doc}
<End Document>"""

output_parser = RegexParser(
    regex=r"Question 1: (.*?)\nCHOIX_A(.*?)\nCHOIX_B(.*?)\nCHOIX_C(.*?)\nCHOIX_D(.*?)(?:\n)+Réponse: (.*)\n\nQuestion 2: (.*?)\nCHOIX_A(.*?)\nCHOIX_B(.*?)\nCHOIX_C(.*?)\nCHOIX_D(.*?)(?:\n)+Réponse: (.*)", 
    output_keys=["question1", "A_1", "B_1", "C_1", "D_1", "reponse1","question2", "A_2", "B_2", "C_2", "D_2", "reponse2"]
)

PROMPT = PromptTemplate(
    input_variables=["doc"], template=template, output_parser=output_parser
)

class QCMGenerateChain(LLMChain):
    """LLM Chain specifically for generating examples for QCM answering."""

    @classmethod
    def from_llm(cls, llm: BaseLLM, **kwargs: Any) -> QCMGenerateChain:
        """Load QA Generate Chain from LLM."""
        return cls(llm=llm, prompt=PROMPT, **kwargs)