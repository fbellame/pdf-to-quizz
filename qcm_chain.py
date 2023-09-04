"""LLM Chain specifically for generating examples for QCM (Question Choix Multiples) answering."""
from __future__ import annotations

from typing import Any
from openllm_chain import OpenLlamaChain
from langchain.chains.llm import LLMChain
from langchain.llms.base import BaseLLM
from langchain.chains.base import Chain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import Any

from langchain.prompts import PromptTemplate

template_openai = "You are a teacher preparing questions for a quiz. Given the following document, please generate 1 multiple-choice questions (MCQs) with 4 options and a corresponding answer letter based on the document. These questions should be detailed and solely based on the information provided in the document.\n{format_instruction}\n{doc}"

template = "|system|You are a teacher preparing questions for a quiz. Given the following document, please generate 1 multiple-choice questions (MCQs) with 4 options and a corresponding answer letter based on the document.\\nExample question:\\nQuestion: question here\\nCHOICE_A: choice here\\nCHOICE_B: choice here\\nCHOICE_C: choice here\\nCHOICE_D: choice here\\nAnswer: A or B or C or D\\nThese questions should be detailed and solely based on the information provided in the document:  |prompt|\\n{doc}\\n\\n |answer|"

class QCM(BaseModel):
    question: str = Field(description="The question of MQC") 
    choice_a: str = Field(description="the choice A")
    choice_b: str = Field(description="the choice B")
    choice_c: str = Field(description="the choice C")
    choice_d: str = Field(description="the choice D")
    answer: str = Field(description="The answer choice_a, choice_b, choice_c or choice_d")

    @validator("question")
    def question_validation(cls, field):
        if field[-1] != '?':
            raise ValueError("question must finish with a question mark ?")
        return field

PROMPT = PromptTemplate(
    input_variables=["doc"], template=template
)

parser = PydanticOutputParser(pydantic_object=QCM)

PROMPT_OPENAI = PromptTemplate(
    input_variables=["doc"], template=template_openai, partial_variables={"format_instruction": parser.get_format_instructions()}
)

class QCMGenerateChainTGI(OpenLlamaChain):
    """LLM Chain specifically for generating examples for QCM answering."""

    @classmethod
    def from_llm(cls, llm: BaseLLM, **kwargs: Any) -> Chain:
        """Load QA Generate Chain from LLM."""
        return cls(llm=llm, prompt=PROMPT, **kwargs)
    
class QCMGenerateChainOpenAI(LLMChain):
    """LLM Chain specifically for generating examples for QCM answering."""

    @classmethod
    def from_llm(cls, llm: BaseLLM, **kwargs: Any) -> Chain:
        """Load QA Generate Chain from LLM."""
        return cls(llm=llm, prompt=PROMPT_OPENAI, **kwargs)