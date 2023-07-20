from langchain.llms import HuggingFacePipeline
import torch
from torch import cuda
from transformers import StoppingCriteria, StoppingCriteriaList
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

# define custom stopping criteria object
class StopOnTokens(StoppingCriteria):

    def __init__(self, tokenizer):

        device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'
        
        self.stop_token_ids = [
            tokenizer.convert_tokens_to_ids(x) for x in [
                ['</s>'], ['User', ':'], ['system', ':'],
                [tokenizer.convert_ids_to_tokens([9427])[0], ':']
            ]
        ]

        # We also need to convert these to `LongTensor` objects:
        self.stop_token_ids = [torch.LongTensor(x).to(device) for x in self.stop_token_ids]

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        for stop_ids in self.stop_token_ids:
            if torch.eq(input_ids[0][-len(stop_ids):], stop_ids).all():
                return True
        return False

class QaLlm():

    def __init__(self) -> None:

        device = 'cuda:0'

        model = transformers.AutoModelForCausalLM.from_pretrained(
           'fbellame/pdf_to_quizz_llama_13B',
           device_map={"": device},
           load_in_4bit=True
        )

        tokenizer = transformers.AutoTokenizer.from_pretrained("fbellame/pdf_to_quizz_llama_13B", use_fast=False)

        stopping_criteria = StoppingCriteriaList([StopOnTokens(tokenizer)])

        generate_text = transformers.pipeline(
            model=model, tokenizer=tokenizer,
            return_full_text=True,  # langchain expects the full text
            task='text-generation',
            device_map={"": device},
            # we pass model parameters here too
            stopping_criteria=stopping_criteria,  # without this model will ramble
            temperature=0.1,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
            top_p=0.15,  # select from top tokens whose probability add up to 15%
            top_k=0,  # select from top 0 tokens (because zero, relies on top_p)
            max_new_tokens=500,  # max number of tokens to generate in the output
            repetition_penalty=1.2  # without this output begins repeating
        )

        self.llm = HuggingFacePipeline(pipeline=generate_text)        

    def get_llm(self):
        return self.llm