from mistral_inference import MistralTextGenInference
from callback import MyCallbackHandler
from langchain.callbacks.base import BaseCallbackManager

class QaLlm():

    def __init__(self) -> None:
        manager = BaseCallbackManager([MyCallbackHandler()])
        self.llm = MistralTextGenInference(inference_server_url="https://75syq57x8ohyw7-8000.proxy.runpod.net", callback_manager=manager)

    def get_llm(self):
        return self.llm