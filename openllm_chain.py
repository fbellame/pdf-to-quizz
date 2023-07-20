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

    def _call_batch(
        self,
        inputs: List[Dict[str, Any]],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> List[Dict[str, str]]:
        
        prompts = []
        for input in inputs:
            prompts.append(self.prompt.format_prompt(**input))

        # generate response from llm
        response = self.llm.generate_prompt(
            prompts,
            callbacks=run_manager.get_child() if run_manager else None
        )

        quizzs = []
        for generation in response.generations:
            quizzs.append({self.output_key: generation[0].text.lstrip()})

        return quizzs

    async def _acall(
        self, inputs: Dict[str, Any], run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, str]:
        raise NotImplementedError("Async is not supported for this chain.")

    @property
    def _chain_type(self) -> str:
        return "open_llama_pdf_to_quizz_chain"
    
    def predict(self, doc: str) -> str:
        
        out = self._call(inputs={'doc': doc})
        return out
    
    def predict_batch(self, docs: List[str], parsers) -> List[str]:

        inputs = []
        for doc in docs:
            inputs.append({'doc': doc})
        
        out = self._call_batch(inputs=inputs)

        ret = []
        for resp in out:
            try:
                ret.append(self.parse(resp, parsers))
            except Exception as e:
                print(f"Error processing page: {str(e)}")
                continue

        return ret

    def predict_and_parse(self, doc: str, parsers) -> str:
        out = self.predict(doc)

        return self.parse(out, parsers)
    
    def parse(self, response: Dict[str, Any], parsers):

        def get_parsed_value(parser, key, doc):
            result = parser.parse(doc["text"])
            value = result.get(key).strip()
            return {key: value}

        quizz = {}
        for key, parser in parsers.items():
            quizz.update(get_parsed_value(parser, key, response))

        return quizz