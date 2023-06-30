from typing import Any, Dict, List, Optional

from langchain.base_language import BaseLanguageModel
from langchain.callbacks.manager import (
    CallbackManagerForChainRun,
)
from langchain.chains.base import Chain
from langchain.prompts.base import BasePromptTemplate
from langchain.output_parsers.regex import RegexParser

class OpenLlamaChain(Chain):
    prompt: BasePromptTemplate
    llm: BaseLanguageModel
    output_key: str = "text"
    suffixes = ['</s>', 'User:', 'system:', 'Assistant:']

    @property
    def input_keys(self) -> List[str]:
        return self.prompt.input_variables
    
    @property
    def output_keys(self) -> List[str]:
        return [self.output_key]
      
    def _call(
        self,
        inputs: Dict[str, Any],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        # format the prompt
        prompt_value = self.prompt.format_prompt(**inputs)
        # generate response from llm
        response = self.llm.generate_prompt(
            [prompt_value],
            callbacks=run_manager.get_child() if run_manager else None
        )
        # _______________
        # here we add the removesuffix logic
        for suffix in self.suffixes:
            response.generations[0][0].text = response.generations[0][0].text.removesuffix(suffix)
        
        return {self.output_key: response.generations[0][0].text.lstrip()}

    async def _acall(
        self, inputs: Dict[str, Any], run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        raise NotImplementedError("Async is not supported for this chain.")

    @property
    def _chain_type(self) -> str:
        return "open_llama_pdf_to_quizz_chain"
    
    def predict(self, doc: str) -> str:
        out = self._call(inputs={'doc': doc})
        return out['text']
    

    def predict_and_parse(self, doc: str, parser: RegexParser) -> str:
        out = self.predict(doc)

        result = parser.parse(out)

        return result
