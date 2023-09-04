from langchain.llms import HuggingFaceTextGenInference
from langchain.llms import OpenAI
from callback import MyCallbackHandler
from langchain.callbacks.base import BaseCallbackManager


class BaseQaLlm():

    def __init__(self) -> None:
        pass

    def get_llm(self):

        return None

class QaLlmTGI(BaseQaLlm):

    def __init__(self) -> None:
        self.llm = HuggingFaceTextGenInference(
            inference_server_url="http://192.168.1.138:8080/",
            max_new_tokens=512,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.2,
            repetition_penalty=1.03,
        )

    def get_llm(self):
        return self.llm
    
class QaLlmOpenAI(BaseQaLlm):

    def __init__(self) -> None:
        manager = BaseCallbackManager([MyCallbackHandler()])
        self.llm = OpenAI(temperature=0, callback_manager=manager, model_name="gpt-3.5-turbo")

    def get_llm(self):
        return self.llm