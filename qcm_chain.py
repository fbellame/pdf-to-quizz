"""LLM Chain specifically for generating examples for QCM (Question Choix Multiples) answering."""
from __future__ import annotations

from typing import Any

from langchain.chains.llm import LLMChain
from langchain.llms.base import BaseLLM
from langchain.output_parsers.regex import RegexParser

from langchain.prompts import PromptTemplate

template = """You are a teacher preparing questions for a quiz. Given the following document, please generate 2 multiple-choice questions (MCQs) with 4 options and a corresponding answer letter based on the document.

Example question:

Question: question here
CHOICE_A: choice here
CHOICE_B: choice here
CHOICE_C: choice here
CHOICE_D: choice here
Answer: A or B or C or D

These questions should be detailed and solely based on the information provided in the document.

<Begin Document>
{doc}
<End Document>"""

output_parser = RegexParser(
    regex=r"Question\s?\d?:\s+\n?(.*?)\nCHOICE_A(.*?)\nCHOICE_B(.*?)\nCHOICE_C(.*?)\nCHOICE_D(.*?)(?:\n)+Answer:\s?(.*)\n?\n?Question\s?\d?:\s+\n?(.*?)\nCHOICE_A(.*?)\nCHOICE_B(.*?)\nCHOICE_C(.*?)\nCHOICE_D(.*?)(?:\n)+Answer:\s?(.*)", 
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