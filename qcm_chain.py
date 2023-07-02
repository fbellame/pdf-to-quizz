"""LLM Chain specifically for generating examples for QCM (Question Choix Multiples) answering."""
from __future__ import annotations

from typing import Any

from openllm_chain import OpenLlamaChain
from langchain.llms.base import BaseLLM

from langchain.prompts import PromptTemplate

instruction = """You are a teacher preparing questions for a quiz. Given the following document, please generate 1 multiple-choice questions (MCQs) with 4 options and a corresponding answer letter based on the document. Example question:\nQuestion: question here\nCHOICE_A: choice here\nCHOICE_B: choice here\nCHOICE_C: choice here\nCHOICE_D: choice here\Answer: A or B or C or D\<Begin Document>\n{doc}\n<End Document>"""
template = f"Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Response:"

# template = """<|prompt|>You are a teacher preparing questions for a quiz. Given the following document, please generate 1 multiple-choice questions (MCQs) with 4 options and a corresponding answer letter based on the document.
#     Example question:
#     Question: question here
#     CHOICE_A: choice here
#     CHOICE_B: choice here
#     CHOICE_C: choice here
#     CHOICE_D: choice here
#     Answer: A or B or C or D
#     <Begin Document>
#     {doc}
#     <End Document></s><|answer|>"""


PROMPT = PromptTemplate(
    input_variables=["doc"], template=template)

class QCMGenerateChain(OpenLlamaChain):
    """LLM Chain specifically for generating examples for QCM answering."""

    @classmethod
    def from_llm(cls, llm: BaseLLM, **kwargs: Any) -> QCMGenerateChain:
        """Load QA Generate Chain from LLM."""
        return cls(llm=llm, prompt=PROMPT, **kwargs)