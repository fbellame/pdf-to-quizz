from langchain.llms import OpenAI
from callback import MyCallbackHandler
from langchain.callbacks.base import BaseCallbackManager

class QaLlm():

    def __init__(self) -> None:
        manager = BaseCallbackManager([MyCallbackHandler()])
        self.llm = OpenAI(temperature=0, callback_manager=manager, model_name="gpt-3.5-turbo")

    def get_llm(self):
        return self.llm